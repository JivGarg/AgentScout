"""
Web Search Service – resolves a company name to a likely official website using Tavily.
Includes lightweight URL safety checks to avoid internal/private targets.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse
import re

import httpx

from app.core.config import get_settings
from app.core.url_safety import is_safe_http_url, is_unsafe_host

settings = get_settings()


class SearchProviderError(Exception):
    """Raised when the search provider is unavailable or misconfigured."""


class NoCompanyWebsiteFoundError(Exception):
    """Raised when no acceptable website candidate is found."""


@dataclass
class SearchMatch:
    resolved_url: str
    source_title: str | None = None
    source_snippet: str | None = None


BLOCKED_RESULT_DOMAINS = {
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "x.com",
    "twitter.com",
    "crunchbase.com",
    "bloomberg.com",
    "wikipedia.org",
    "youtube.com",
    "angel.co",
    "wellfound.com",
}


def _tokenize(text: str) -> set[str]:
    return {t for t in re.split(r"[^a-zA-Z0-9]+", text.lower()) if len(t) > 2}


def _provider_endpoint() -> str:
    """Validate and return Tavily endpoint URL."""
    base_url = (settings.TAVILY_BASE_URL or "").strip()
    if not base_url:
        raise SearchProviderError("TAVILY_BASE_URL is not configured.")

    parsed = urlparse(base_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise SearchProviderError("TAVILY_BASE_URL must be a valid https URL.")

    provider_host = parsed.netloc.lower().split(":", 1)[0]
    if is_unsafe_host(provider_host):
        raise SearchProviderError("TAVILY_BASE_URL points to an unsafe host.")

    return base_url.rstrip("/") + "/search"


def _score_candidate(company_name: str, url: str, title: str | None) -> int:
    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")
    path = parsed.path or "/"

    company_tokens = _tokenize(company_name)
    host_tokens = _tokenize(host)
    title_tokens = _tokenize(title or "")

    overlap_score = len(company_tokens.intersection(host_tokens)) * 25
    overlap_score += len(company_tokens.intersection(title_tokens)) * 10

    score = overlap_score

    # Root/home pages are usually official sites.
    if path in {"", "/"}:
        score += 20

    # De-prioritize known directories/social properties.
    for blocked in BLOCKED_RESULT_DOMAINS:
        if host.endswith(blocked):
            score -= 60
            break

    if len(path) > 40:
        score -= 10

    return score


async def search_company_website(company_name: str) -> SearchMatch:
    """
    Find the best website candidate for a company name using Tavily.

    Returns:
        SearchMatch with resolved_url and optional source metadata.

    Raises:
        SearchProviderError: provider key missing, timeout, or bad provider response.
        NoCompanyWebsiteFoundError: no safe/credible website candidate found.
    """
    company_name = (company_name or "").strip()
    if not company_name:
        raise NoCompanyWebsiteFoundError("Company name is empty.")

    if not settings.TAVILY_API_KEY:
        raise SearchProviderError("TAVILY_API_KEY is not configured.")

    endpoint = _provider_endpoint()
    payload = {
        "api_key": settings.TAVILY_API_KEY,
        "query": f"{company_name} official website",
        "search_depth": "basic",
        "max_results": 8,
        "include_answer": False,
        "include_images": False,
        "include_raw_content": False,
    }

    try:
        async with httpx.AsyncClient(timeout=12.0) as client:
            response = await client.post(endpoint, json=payload)
    except httpx.TimeoutException as exc:
        raise SearchProviderError("Search provider timed out.") from exc
    except httpx.HTTPError as exc:
        raise SearchProviderError("Search provider request failed.") from exc

    if response.status_code >= 400:
        raise SearchProviderError(f"Search provider error: HTTP {response.status_code}")

    try:
        data = response.json()
    except ValueError as exc:
        raise SearchProviderError("Search provider returned invalid JSON.") from exc

    results = data.get("results") or []
    if not isinstance(results, list) or not results:
        raise NoCompanyWebsiteFoundError("No search results found for this company.")

    scored: list[tuple[int, dict]] = []
    for result in results:
        if not isinstance(result, dict):
            continue

        url = str(result.get("url", "")).strip()
        title = result.get("title")

        if not is_safe_http_url(url):
            continue

        score = _score_candidate(company_name, url, title)
        scored.append((score, result))

    if not scored:
        raise NoCompanyWebsiteFoundError("No safe website candidates found.")

    scored.sort(key=lambda x: x[0], reverse=True)
    best_score = scored[0][0]
    if best_score < 10:
        raise NoCompanyWebsiteFoundError("Unable to confidently identify an official website.")

    best = scored[0][1]

    resolved_url = str(best.get("url", "")).strip()
    if not resolved_url:
        raise NoCompanyWebsiteFoundError("Unable to resolve a target website.")

    source_title = best.get("title") or None
    source_snippet = best.get("content") or None
    if isinstance(source_title, str) and len(source_title) > 200:
        source_title = source_title[:200]
    if isinstance(source_snippet, str) and len(source_snippet) > 500:
        source_snippet = source_snippet[:500]

    return SearchMatch(
        resolved_url=resolved_url,
        source_title=source_title,
        source_snippet=source_snippet,
    )
