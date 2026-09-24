from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl


# ── Auth Schemas ──────────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Research Schemas ──────────────────────────────────────────
class ResearchRequest(BaseModel):
    url: HttpUrl


class CompanyResearchRequest(BaseModel):
    company_name: str = Field(min_length=2, max_length=120)


class ResearchResult(BaseModel):
    company_name: str
    summary: str
    pain_points: list[str]
    generated_pitch: str


class ResearchResponse(BaseModel):
    id: int
    target_url: str
    company_name: Optional[str]
    summary: Optional[str]
    pain_points: list[str]
    generated_pitch: Optional[str]
    timestamp: datetime

    model_config = {"from_attributes": True}


class CompanyResearchResponse(ResearchResponse):
    searched_company_name: str
    resolved_url: str
    search_source_title: Optional[str] = None
    search_source_snippet: Optional[str] = None


# ── Resume Schemas ────────────────────────────────────────────
class ResumeAnalyzeRequest(BaseModel):
    resume_text: str


class ResumeSectionScore(BaseModel):
    section: str
    score: int          # 0-100
    feedback: str
    suggestions: list[str]


class ResumeAnalyzeResponse(BaseModel):
    overall_score: int  # 0-100
    grade: str          # A / B / C / D / F
    summary: str
    section_scores: list[ResumeSectionScore]
    red_flags: list[str]
    strong_points: list[str]
    rewritten_bullets: list[str]  # up to 3 XYZ-formula rewrites


# ── Search History Schemas ────────────────────────────────────
class SearchLogResponse(BaseModel):
    id: int
    target_url: str
    company_name: Optional[str]
    summary: Optional[str]
    pain_points: list[str]
    generated_pitch: Optional[str]
    timestamp: datetime

    model_config = {"from_attributes": True}
