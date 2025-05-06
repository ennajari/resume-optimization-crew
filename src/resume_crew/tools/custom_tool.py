from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pdfplumber
from pathlib import Path

class ResumeParserInput(BaseModel):
    """Input schema for ResumeParserTool."""
    resume_path: str = Field(..., description="Path to the resume PDF file.")

class ResumeParserTool(BaseTool):
    name: str = "ResumeParserTool"
    description: str = (
        "Extracts text content from a PDF resume file for further processing."
    )
    args_schema: Type[BaseModel] = ResumeParserInput

    def _run(self, resume_path: str) -> str:
        try:
            resume_path = Path(resume_path)
            if not resume_path.exists():
                return f"Error: Resume file not found at {resume_path}"
            with pdfplumber.open(resume_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                if not text.strip():
                    return "Error: No text extracted from resume PDF"
                return text
        except Exception as e:
            return f"Error processing resume: {str(e)}"