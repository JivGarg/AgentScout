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

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from app.core.config import get_settings

settings = get_settings()


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
rewritten_bullets (array of up to 3 strings using XYZ formula from weak bullets you found)""",
        ),
        (
            "human",
            """Evaluate this resume:

---
{resume_text}
---

Return JSON only.""",
        ),
    ]
)


# ── Main Function ─────────────────────────────────────────────

def _get_llm() -> ChatOpenAI:
    """
    Returns the LLM instance.
    Uses local Ollama by default; falls back to OpenAI if OPENAI_API_KEY is set.
    """
    openai_key = (settings.OPENAI_API_KEY or "").strip()
    use_openai = openai_key and not openai_key.startswith("sk-your-")

    if use_openai:
        print("[resume_analyzer] Using OpenAI")
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=openai_key,
        )

    print(f"[resume_analyzer] Using Ollama ({settings.OLLAMA_MODEL}) at {settings.OLLAMA_BASE_URL}")
    return ChatOpenAI(
        model=settings.OLLAMA_MODEL,
        temperature=0.3,
        api_key="ollama",
        base_url=f"{settings.OLLAMA_BASE_URL}/v1",
    )


async def analyze_resume(resume_text: str) -> dict:
    """
    Analyze a resume text and return structured feedback.

    Args:
        resume_text: The raw text of the resume pasted by the user.

    Returns:
        dict with keys: overall_score, grade, summary, section_scores,
                        red_flags, strong_points, rewritten_bullets
    """
    llm = _get_llm()
    parser = JsonOutputParser(pydantic_object=ResumeAnalysis)
    chain = RESUME_PROMPT | llm | parser

    try:
        result = await chain.ainvoke({"resume_text": resume_text})
        return result
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
