from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class SkillScore(BaseModel):
    skill_name: str = Field(description="Name of the skill being scored")
    required: bool = Field(description="Whether this skill is required or nice-to-have")
    match_level: float = Field(description="How well the candidate's experience matches (0-1)", ge=0, le=1)
    years_experience: Optional[float] = Field(description="Years of experience with this skill", default=None)
    context_score: float = Field(
        description="Relevance of skill usage to job requirements", ge=0, le=1, default=0.5
    )

class JobMatchScore(BaseModel):
    overall_match: float = Field(description="Overall match percentage (0-100)", ge=0, le=100)
    technical_skills_match: float = Field(description="Technical skills match percentage", ge=0, le=100)
    soft_skills_match: float = Field(description="Soft skills match percentage", ge=0, le=100)
    experience_match: float = Field(description="Experience level match percentage", ge=0, le=100)
    education_match: float = Field(description="Education requirements match percentage", ge=0, le=100)
    industry_match: float = Field(description="Industry experience match percentage", ge=0, le=100)
    skill_details: List[SkillScore] = Field(description="Detailed scoring for each skill", default_factory=list)
    strengths: List[str] = Field(description="Candidate strengths", default_factory=list)
    gaps: List[str] = Field(description="Areas needing improvement", default_factory=list)
    scoring_factors: Dict[str, float] = Field(
        description="Weights for scoring components",
        default_factory=lambda: {
            "technical_skills": 0.35,
            "soft_skills": 0.20,
            "experience": 0.25,
            "education": 0.10,
            "industry": 0.10
        }
    )

class JobRequirements(BaseModel):
    technical_skills: List[str] = Field(description="Required technical skills", default_factory=list)
    soft_skills: List[str] = Field(description="Required soft skills", default_factory=list)
    experience_requirements: List[str] = Field(description="Experience requirements", default_factory=list)
    key_responsibilities: List[str] = Field(description="Key job responsibilities", default_factory=list)
    education_requirements: List[str] = Field(description="Education requirements", default_factory=list)
    nice_to_have: List[str] = Field(description="Preferred skills", default_factory=list)
    job_title: str = Field(description="Job title", default="")
    department: Optional[str] = Field(description="Department or team", default=None)
    job_level: Optional[str] = Field(description="Position level", default=None)
    location_requirements: Dict[str, str] = Field(description="Location details", default_factory=dict)
    compensation: Dict[str, str] = Field(description="Compensation details", default_factory=dict)
    benefits: List[str] = Field(description="Benefits and perks", default_factory=list)
    tools_and_technologies: List[str] = Field(description="Tools/technologies used", default_factory=list)
    industry_knowledge: List[str] = Field(description="Industry-specific knowledge", default_factory=list)
    certifications_required: List[str] = Field(description="Required certifications", default_factory=list)
    job_url: str = Field(description="Job posting URL", default="")
    match_score: JobMatchScore = Field(description="Candidate match scoring")
    score_explanation: List[str] = Field(description="Scoring explanation", default_factory=list)

class ResumeOptimization(BaseModel):
    content_suggestions: List[Dict[str, str]] = Field(description="Content optimization suggestions", default_factory=list)
    skills_to_highlight: List[str] = Field(description="Skills to emphasize", default_factory=list)
    achievements_to_add: List[str] = Field(description="Achievements to add/modify", default_factory=list)
    keywords_for_ats: List[str] = Field(description="ATS keywords", default_factory=list)
    formatting_suggestions: List[str] = Field(description="Formatting improvements", default_factory=list)

class CompanyResearch(BaseModel):
    recent_developments: List[str] = Field(description="Recent company news", default_factory=list)
    culture_and_values: List[str] = Field(description="Company culture and values", default_factory=list)
    market_position: Dict[str, List[str]] = Field(description="Market position and competitors", default_factory=dict)
    growth_trajectory: List[str] = Field(description="Company growth plans", default_factory=list)
    interview_questions: List[str] = Field(description="Strategic interview questions", default_factory=list)
    
    # Model method to convert to valid JSON
    def json(self, **kwargs):
        return super().model_dump_json(**kwargs)

class CoverLetter(BaseModel):
    """Model for a generated cover letter with structured sections"""
    name: str = Field(description="Candidate's full name")
    address: str = Field(description="Candidate's address")
    email: str = Field(description="Candidate's email address")
    phone: str = Field(description="Candidate's phone number")
    
    company_contact: str = Field(default="", description="Name of the contact at the company (optional)")
    company_name: str = Field(description="Company name")
    company_address: str = Field(default="", description="Company address (optional)")
    
    date: str = Field(description="Date of the letter")
    subject: str = Field(description="Subject line of the application")

    opening_paragraph: str = Field(description="Engaging opening paragraph")
    experience_paragraphs: List[str] = Field(description="Paragraphs highlighting relevant experience")
    company_alignment_paragraph: str = Field(description="Paragraph showing alignment with company")
    closing_paragraph: str = Field(description="Closing paragraph with call to action")

    def json(self, **kwargs):
        return super().model_dump_json(**kwargs)
