"""
Research API – the core endpoint that scrapes a URL and returns AI-generated analysis.
"""

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.search_log import SearchLog
from app.schemas.schemas import (
    CompanyResearchRequest,
    CompanyResearchResponse,
    ResearchRequest,
    ResearchResponse,
    SearchLogResponse,
)
from app.services.scraper import scrape_url
from app.services.researcher import LLMNotConfiguredError, analyze_company
from app.services.web_search import (
    NoCompanyWebsiteFoundError,
    SearchProviderError,
    search_company_website,
)

router = APIRouter(prefix="/research", tags=["Research"])


async def _save_research_log(
    db: AsyncSession,
    user_id: int,
    url: str,
    raw_content: str,
    research: dict,
) -> SearchLog:
    """Persist research output and return the created ORM row."""
    search_log = SearchLog(
        user_id=user_id,
        target_url=url,
        raw_content=raw_content,
        company_name=research.get("company_name", ""),
        summary=research.get("summary", ""),
        pain_points=json.dumps(research.get("pain_points", [])),
        generated_pitch=research.get("generated_pitch", ""),
    )
    db.add(search_log)
    await db.flush()
    await db.refresh(search_log)
    return search_log


def _to_research_response(search_log: SearchLog, research: dict) -> ResearchResponse:
    """Create a API response model from a persisted search log + parsed research."""
    pain_points = research.get("pain_points")
    if not isinstance(pain_points, list):
        pain_points = []

    return ResearchResponse(
        id=search_log.id,
        target_url=search_log.target_url,
        company_name=search_log.company_name,
        summary=search_log.summary,
        pain_points=pain_points,
        generated_pitch=search_log.generated_pitch,
        timestamp=search_log.timestamp,
    )


@router.post("/analyze", response_model=ResearchResponse)
async def analyze_url(
    request: ResearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Main endpoint: Takes a URL, scrapes it, runs AI analysis,
    stores the result, and returns structured research data.
    """
    url = str(request.url)

    # Step 1: Scrape the website
    try:
        raw_content = await scrape_url(url)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    # Step 2: Run AI analysis
    try:
        research = await analyze_company(url, raw_content)
    except LLMNotConfiguredError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured. Set GEMINI_API_KEY on the server.",
        )

    # Step 3: Store in database
    search_log = await _save_research_log(
        db=db,
        user_id=current_user.id,
        url=url,
        raw_content=raw_content,
        research=research,
    )

    # Step 4: Return response
    return _to_research_response(search_log, research)


@router.post("/analyze-company", response_model=CompanyResearchResponse)
async def analyze_company_name(
    request: CompanyResearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    One-step company analysis:
    1) Resolve a company name to website using Tavily
    2) Scrape website content
    3) Run AI analysis
    4) Persist to history
    """
    company_name = request.company_name.strip()

    # Step 1: Resolve company name to a likely official website.
    try:
        match = await search_company_website(company_name)
    except NoCompanyWebsiteFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except SearchProviderError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    # Step 2: Scrape resolved URL.
    try:
        raw_content = await scrape_url(match.resolved_url)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    # Step 3: Run AI analysis.
    try:
        research = await analyze_company(match.resolved_url, raw_content)
    except LLMNotConfiguredError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured. Set GEMINI_API_KEY on the server.",
        )

    # Step 4: Save and return.
    search_log = await _save_research_log(
        db=db,
        user_id=current_user.id,
        url=match.resolved_url,
        raw_content=raw_content,
        research=research,
    )
    base_response = _to_research_response(search_log, research)

    return CompanyResearchResponse(
        **base_response.model_dump(),
        searched_company_name=company_name,
        resolved_url=match.resolved_url,
        search_source_title=match.source_title,
        search_source_snippet=match.source_snippet,
    )


@router.get("/history", response_model=list[SearchLogResponse])
async def get_search_history(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the authenticated user's research history."""
    result = await db.execute(
        select(SearchLog)
        .where(SearchLog.user_id == current_user.id)
        .order_by(desc(SearchLog.timestamp))
        .offset(skip)
        .limit(limit)
    )
    logs = result.scalars().all()

    response = []
    for log in logs:
        try:
            pain_points = json.loads(log.pain_points) if log.pain_points else []
        except (json.JSONDecodeError, TypeError):
            pain_points = []

        response.append(
            SearchLogResponse(
                id=log.id,
                target_url=log.target_url,
                company_name=log.company_name,
                summary=log.summary,
                pain_points=pain_points,
                generated_pitch=log.generated_pitch,
                timestamp=log.timestamp,
            )
        )
    return response


@router.get("/history/{log_id}", response_model=SearchLogResponse)
async def get_search_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific research result by ID."""
    result = await db.execute(
        select(SearchLog).where(
            SearchLog.id == log_id,
            SearchLog.user_id == current_user.id,
        )
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research not found")

    try:
        pain_points = json.loads(log.pain_points) if log.pain_points else []
    except (json.JSONDecodeError, TypeError):
        pain_points = []

    return SearchLogResponse(
        id=log.id,
        target_url=log.target_url,
        company_name=log.company_name,
        summary=log.summary,
        pain_points=pain_points,
        generated_pitch=log.generated_pitch,
        timestamp=log.timestamp,
    )


@router.delete("/history/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_search_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a specific research result."""
    result = await db.execute(
        select(SearchLog).where(
            SearchLog.id == log_id,
            SearchLog.user_id == current_user.id,
        )
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Research not found")

    await db.delete(log)
    return None
