"""
Resume API – endpoint for analyzing a student's resume text.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.schemas import ResumeAnalyzeRequest, ResumeAnalyzeResponse
from app.services.resume_analyzer import LLMNotConfiguredError, analyze_resume

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/analyze", response_model=ResumeAnalyzeResponse)
async def analyze_resume_endpoint(
    request: ResumeAnalyzeRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Accepts raw resume text and returns structured AI feedback:
    - Overall score (0-100) and letter grade
    - Per-section scores (Header, Summary, Experience, Skills, Education, Formatting)
    - Red-flag phrases detected
    - Strong points
    - Up to 3 bullet rewrites using the XYZ formula
    """
    if not request.resume_text or len(request.resume_text.strip()) < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text is too short. Please paste the full text of your resume.",
        )

    if len(request.resume_text) > 15_000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text exceeds the 15,000 character limit. Please shorten it.",
        )

    try:
        result = await analyze_resume(request.resume_text)
    except LLMNotConfiguredError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured. Set GEMINI_API_KEY on the server.",
        )
    return ResumeAnalyzeResponse(**result)
