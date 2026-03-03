"""
AI Researcher Service – analyzes scraped content using LangChain + Ollama (llama3)
with optional OpenAI fallback.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from app.core.config import get_settings

settings = get_settings()


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

Be concise. No markdown, no explanation outside the JSON.""",
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
        content: The scraped text content from the website.

    Returns:
        dict with keys: company_name, summary, pain_points, generated_pitch
    """
    llm = _get_llm()

    parser = JsonOutputParser(pydantic_object=CompanyResearch)

    chain = RESEARCH_PROMPT | llm | parser

    try:
        result = await chain.ainvoke({"url": url, "content": content})
        return result
    except Exception as e:
        print(f"[researcher] LLM analysis error: {e}")
        # Return a fallback structure
        return {
            "company_name": _extract_domain(url),
            "summary": "Unable to generate summary. Please try again.",
            "pain_points": ["Analysis failed – please retry"],
            "generated_pitch": "Unable to generate pitch. The content may be too short or inaccessible.",
        }


def _get_llm():
    """
    Returns the LLM instance.
    Uses local Ollama (llama3) by default.
    Falls back to OpenAI if OPENAI_API_KEY is set.
    """
    openai_key = (settings.OPENAI_API_KEY or "").strip()
    use_openai = openai_key and not openai_key.startswith("sk-your-")

    if use_openai:
        print("[researcher] Using OpenAI")
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.4,
            api_key=openai_key,
        )

    # Ollama exposes an OpenAI-compatible API at /v1
    print(f"[researcher] Using Ollama ({settings.OLLAMA_MODEL}) at {settings.OLLAMA_BASE_URL}")
    return ChatOpenAI(
        model=settings.OLLAMA_MODEL,
        temperature=0.4,
        api_key="ollama",  # Ollama doesn't need a real key but the field is required
        base_url=f"{settings.OLLAMA_BASE_URL}/v1",
    )


def _extract_domain(url: str) -> str:
    """Extract a readable domain name from a URL."""
    from urllib.parse import urlparse

    parsed = urlparse(str(url))
    domain = parsed.netloc or parsed.path
    domain = domain.replace("www.", "")
    return domain.split(".")[0].capitalize()
