"""
AI Researcher Service – analyzes scraped content using LangChain + Gemini Flash.
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

MAX_CONTENT_CHARS = 5000
MAX_PAIN_POINTS = 5
MAX_FIELD_LEN = 2000


class LLMNotConfiguredError(RuntimeError):
    """Raised when no LLM API key is configured — a deployment issue, not a transient failure."""


# ── Pydantic model for structured AI output ───────────────────
class CompanyResearch(BaseModel):
    company_name: str = Field(description="The name of the company")
    summary: str = Field(description="A 2-3 sentence summary of what the company does")
    pain_points: list[str] = Field(
        description="A list of 3-5 potential pain points or challenges the company might face"
    )
    generated_pitch: str = Field(
        description="A 3-paragraph personalized cold outreach email draft"
    )


# ── Prompt Templates ──────────────────────────────────────────

RESEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a B2B sales researcher. Analyze company websites and return ONLY valid JSON.

Return JSON with these keys:
- "company_name": string (the company name)
- "summary": string (2 sentences max about what they do)
- "pain_points": array of 3 short strings (business challenges they likely face)
- "generated_pitch": string (3 short paragraphs: 1. mention something specific about them, 2. identify a pain point, 3. suggest a quick call)

Be concise. No markdown, no explanation outside the JSON.

"""
            + ANTI_INJECTION_CLAUSE,
        ),
        (
            "human",
            """Website: {url}

Content:
{content}

Return JSON only.""",
        ),
    ]
)


# ── Main Research Function ────────────────────────────────────

async def analyze_company(url: str, content: str) -> dict:
    """
    Use LLM to analyze scraped website content and produce structured research.

    Args:
        url: The target company URL.
        content: The scraped text content from the website (untrusted, third-party).

    Returns:
        dict with keys: company_name, summary, pain_points, generated_pitch
    """
    safe_content = sanitize_untrusted_text(content, MAX_CONTENT_CHARS)
    if looks_like_injection(safe_content):
        print(f"[researcher] possible prompt-injection content detected for {url}")

    wrapped_content = wrap_untrusted(safe_content, "WEBSITE_CONTENT")

    llm = _get_llm()  # raises LLMNotConfiguredError if no API key — let that propagate
    parser = JsonOutputParser(pydantic_object=CompanyResearch)
    chain = RESEARCH_PROMPT | llm | parser

    try:
        result = await chain.ainvoke({"url": url, "content": wrapped_content})
        return _clamp_result(result, url)
    except Exception as e:
        print(f"[researcher] LLM analysis error: {e}")
        # Return a fallback structure
        return {
            "company_name": _extract_domain(url),
            "summary": "Unable to generate summary. Please try again.",
            "pain_points": ["Analysis failed – please retry"],
            "generated_pitch": "Unable to generate pitch. The content may be too short or inaccessible.",
        }


def _clamp_result(result: dict, url: str) -> dict:
    """
    Enforce hard size/shape limits on whatever the model returned, so that
    even a successful injection can only distort text within fixed bounds —
    never inject extra keys, oversized payloads, or non-string content.
    """
    if not isinstance(result, dict):
        return {
            "company_name": _extract_domain(url),
            "summary": "Unable to generate summary. Please try again.",
            "pain_points": [],
            "generated_pitch": "",
        }

    return {
        "company_name": clamp_string(result.get("company_name"), 200, _extract_domain(url)),
        "summary": clamp_string(result.get("summary"), MAX_FIELD_LEN),
        "pain_points": clamp_list_of_strings(result.get("pain_points"), MAX_PAIN_POINTS, 300),
        "generated_pitch": clamp_string(result.get("generated_pitch"), MAX_FIELD_LEN),
    }


def _get_llm():
    """Returns the Gemini Flash LLM instance."""
    gemini_key = (settings.GEMINI_API_KEY or "").strip()
    if not gemini_key:
        raise LLMNotConfiguredError("No LLM configured: set GEMINI_API_KEY in .env")

    print(f"[researcher] Using Gemini ({settings.GEMINI_MODEL})")
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        temperature=0.4,
        google_api_key=gemini_key,
    )


def _extract_domain(url: str) -> str:
    """Extract a readable domain name from a URL."""
    from urllib.parse import urlparse

    parsed = urlparse(str(url))
    domain = parsed.netloc or parsed.path
    domain = domain.replace("www.", "")
    return domain.split(".")[0].capitalize()
