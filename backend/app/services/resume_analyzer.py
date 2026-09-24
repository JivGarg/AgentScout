"""
Resume Analyzer Service
Evaluates a student/professional resume against the criteria outlined in cvStruct.md:
  - Measurable impact (XYZ formula)
  - Action verb quality
  - Section completeness (Header, Experience, Skills, Education)
  - Red-flag phrases ("responsible for", "helped with", "references available", etc.)
  - Professional summary presence & quality
  - White-space / readability signals (detected through structural clues in text)
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.core.guardrails import (
    ANTI_INJECTION_CLAUSE,
    clamp_list_of_strings,
    clamp_string,
    looks_like_injection,
    sanitize_untrusted_text,
    wrap_untrusted,
)

settings = get_settings()

MAX_RESUME_CHARS = 15_000
VALID_GRADES = {"A", "B", "C", "D", "F"}


class LLMNotConfiguredError(RuntimeError):
    """Raised when no LLM API key is configured — a deployment issue, not a transient failure."""


# ── Pydantic model for structured AI output ───────────────────
class SectionScore(BaseModel):
    section: str = Field(description="Name of the resume section")
    score: int = Field(description="Score from 0 to 100")
    feedback: str = Field(description="One-sentence feedback")
    suggestions: list[str] = Field(description="1-3 concrete improvement suggestions")


class ResumeAnalysis(BaseModel):
    overall_score: int = Field(description="Overall resume score 0-100")
    grade: str = Field(description="Letter grade: A, B, C, D, or F")
    summary: str = Field(description="2-3 sentence executive summary of the resume quality")
    section_scores: list[SectionScore] = Field(description="Scores for each main section")
    red_flags: list[str] = Field(description="List of weak phrases or mistakes found verbatim")
    strong_points: list[str] = Field(description="List of 2-4 things done well")
    rewritten_bullets: list[str] = Field(
        description="Up to 3 bullet points rewritten using the XYZ formula: [Action Verb] + [Task] + [Quantifiable Result]"
    )


# ── Prompt ────────────────────────────────────────────────────

RESUME_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert resume coach and recruiter. You evaluate resumes based on these strict criteria:

=== SCORING CRITERIA ===
1. HEADER (10 pts): Has name, professional email (firstname.lastname@), LinkedIn/Portfolio link.
   Deduct if: physical address included (privacy risk), unprofessional email.

2. PROFESSIONAL SUMMARY (15 pts): 3 lines or fewer. Tells what the candidate OFFERS, not what they WANT.
   Deduct if: it is an "Objective" statement ("I am looking for...") instead of a value proposition.

3. EXPERIENCE SECTION (35 pts): Reverse-chronological. Each bullet uses the XYZ formula:
   [Action Verb] + [Specific Task] + [Quantifiable Result]
   Strong action verbs: Spearheaded, Orchestrated, Launched, Architected, Reduced, Maximised, Yielded, etc.
   Weak verbs to flag: "Responsible for", "Helped with", "Worked on", "Assisted", "Did"
   Deduct for: passive language, missing numbers/%, vague tasks, no career progression shown.

4. SKILLS SECTION (20 pts): Hard skills (technical) separated from Soft skills (interpersonal).
   Deduct if: skills are buried in paragraph form, or jargon/acronyms without context.

5. EDUCATION SECTION (10 pts): Recent first. Honors included if graduated in last 3 years.
   Deduct if: older than 3 years and still listing GPA/honors that are not exceptional.

6. FORMATTING & CLEANLINESS (10 pts): No "References available upon request", no full physical address,
   no unprofessional content. Clean bullet structure implied by text.

=== RED-FLAG PHRASES (always call these out) ===
- "Responsible for"
- "Helped with"
- "Worked on"
- "Assisted"
- "References available upon request"
- "Dynamic", "Passionate", "Hardworking" (overused buzzwords without evidence)
- Any objective statement like "Seeking a position..."

=== OUTPUT FORMAT ===
Return ONLY valid JSON with no markdown, no explanation outside the JSON.
Keys: overall_score (int 0-100), grade (A/B/C/D/F), summary (string),
section_scores (array of objects with section/score/feedback/suggestions),
red_flags (array of strings), strong_points (array of strings),
rewritten_bullets (array of up to 3 strings using XYZ formula from weak bullets you found)

"""
            + ANTI_INJECTION_CLAUSE,
        ),
        (
            "human",
            """Evaluate this resume:

{resume_text}

Return JSON only.""",
        ),
    ]
)


# ── Main Function ─────────────────────────────────────────────

def _get_llm():
    """Returns the Gemini Flash LLM instance."""
    gemini_key = (settings.GEMINI_API_KEY or "").strip()
    if not gemini_key:
        raise LLMNotConfiguredError("No LLM configured: set GEMINI_API_KEY in .env")

    print(f"[resume_analyzer] Using Gemini ({settings.GEMINI_MODEL})")
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        temperature=0.3,
        google_api_key=gemini_key,
    )


def _clamp_section_scores(value) -> list[dict]:
    if not isinstance(value, list):
        return []
    out = []
    for item in value[:10]:
        if not isinstance(item, dict):
            continue
        try:
            score = int(item.get("score", 0))
        except (TypeError, ValueError):
            score = 0
        score = max(0, min(100, score))
        out.append(
            {
                "section": clamp_string(item.get("section"), 100, "Section"),
                "score": score,
                "feedback": clamp_string(item.get("feedback"), 500),
                "suggestions": clamp_list_of_strings(item.get("suggestions"), 3, 300),
            }
        )
    return out


def _clamp_result(result: dict) -> dict:
    """Enforce hard size/shape/range limits on the model's output."""
    if not isinstance(result, dict):
        result = {}

    try:
        overall_score = max(0, min(100, int(result.get("overall_score", 0))))
    except (TypeError, ValueError):
        overall_score = 0

    grade = clamp_string(result.get("grade"), 1).upper()
    if grade not in VALID_GRADES:
        grade = "F"

    return {
        "overall_score": overall_score,
        "grade": grade,
        "summary": clamp_string(result.get("summary"), 1000),
        "section_scores": _clamp_section_scores(result.get("section_scores")),
        "red_flags": clamp_list_of_strings(result.get("red_flags"), 20, 300),
        "strong_points": clamp_list_of_strings(result.get("strong_points"), 10, 300),
        "rewritten_bullets": clamp_list_of_strings(result.get("rewritten_bullets"), 3, 500),
    }


async def analyze_resume(resume_text: str) -> dict:
    """
    Analyze a resume text and return structured feedback.

    Args:
        resume_text: The raw text of the resume pasted by the user (untrusted input).

    Returns:
        dict with keys: overall_score, grade, summary, section_scores,
                        red_flags, strong_points, rewritten_bullets
    """
    safe_text = sanitize_untrusted_text(resume_text, MAX_RESUME_CHARS)
    if looks_like_injection(safe_text):
        print("[resume_analyzer] possible prompt-injection content detected in resume")

    wrapped_text = wrap_untrusted(safe_text, "RESUME_TEXT")

    llm = _get_llm()
    parser = JsonOutputParser(pydantic_object=ResumeAnalysis)
    chain = RESUME_PROMPT | llm | parser

    try:
        result = await chain.ainvoke({"resume_text": wrapped_text})
        return _clamp_result(result)
    except Exception as e:
        print(f"[resume_analyzer] LLM error: {e}")
        # Return a safe fallback rather than crashing
        return {
            "overall_score": 0,
            "grade": "F",
            "summary": "Could not analyze the resume due to an AI error. Please try again.",
            "section_scores": [],
            "red_flags": [],
            "strong_points": [],
            "rewritten_bullets": [],
        }
