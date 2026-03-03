"""
Scraper Service – extracts clean text content from a target URL.
Uses Crawl4AI as the primary scraper with httpx as fallback.
"""

import httpx
from typing import Optional


async def scrape_url_with_crawl4ai(url: str) -> Optional[str]:
    """
    Scrape a URL using Crawl4AI for clean markdown extraction.
    Handles bot-blockers and JavaScript-rendered pages.
    """
    try:
        from crawl4ai import AsyncWebCrawler

        async with AsyncWebCrawler(verbose=False) as crawler:
            result = await crawler.arun(url=url)
            if result and result.markdown:
                return result.markdown.strip()
    except ImportError:
        print("[scraper] crawl4ai not installed, falling back to httpx")
    except Exception as e:
        print(f"[scraper] crawl4ai error: {e}")
    return None


# Sites known to aggressively block scrapers
BLOCKED_DOMAINS = ["linkedin.com", "facebook.com", "instagram.com"]


def _is_blocked_domain(url: str) -> bool:
    from urllib.parse import urlparse
    domain = urlparse(str(url)).netloc.lower().replace("www.", "")
    return any(domain.endswith(b) for b in BLOCKED_DOMAINS)


async def scrape_url_with_httpx(url: str) -> Optional[str]:
    """
    Scraper using httpx + BeautifulSoup for clean text extraction.
    Handles non-standard status codes (e.g. LinkedIn 999) gracefully.
    """
    try:
        from bs4 import BeautifulSoup
        import re

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            response = await client.get(str(url), headers=headers)

            # Accept any response that has HTML body (some sites return non-standard codes)
            if response.status_code >= 400:
                # Still try to parse if we got HTML back
                if response.text and len(response.text) > 500:
                    print(f"[scraper] got status {response.status_code} but will try to parse body")
                else:
                    print(f"[scraper] blocked by site: HTTP {response.status_code}")
                    return None

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove non-content elements
            for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg", "iframe"]):
                tag.decompose()

            text = soup.get_text(separator="\n", strip=True)
            # Collapse blank lines
            text = re.sub(r"\n{3,}", "\n\n", text)

            # If we got very little text, consider it failed
            if len(text.strip()) < 100:
                print(f"[scraper] page returned too little text ({len(text)} chars)")
                return None

            return text
    except Exception as e:
        print(f"[scraper] httpx error: {e}")
    return None


async def scrape_url(url: str) -> str:
    """
    Main scraper function. Tries Crawl4AI first, falls back to httpx.
    Returns cleaned text content from the given URL.

    Raises:
        ValueError: If scraping fails with all methods.
    """
    # Early check for known-blocked domains
    if _is_blocked_domain(url):
        raise ValueError(
            f"This site blocks automated access (bot protection). "
            f"Try a public company website instead (e.g. stripe.com, notion.so)."
        )

    # Try Crawl4AI first (best quality)
    content = await scrape_url_with_crawl4ai(url)
    if content:
        return _truncate_content(content)

    # Fallback to httpx
    content = await scrape_url_with_httpx(url)
    if content:
        return _truncate_content(content)

    raise ValueError(
        f"Could not extract content from {url}. "
        f"The site may be blocking scrapers or requires JavaScript rendering."
    )


def _truncate_content(content: str, max_chars: int = 5000) -> str:
    """Truncate content aggressively for fast local LLM inference."""
    if len(content) > max_chars:
        return content[:max_chars] + "\n\n[Content truncated...]"
    return content
