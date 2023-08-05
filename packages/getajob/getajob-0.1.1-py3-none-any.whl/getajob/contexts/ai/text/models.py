from pydantic import BaseModel


class ExtractKeywords(BaseModel):
    text: str
    max_tokens: int = 60


class GenerateInterviewQuestions(BaseModel):
    job_name: str
    max_tokens: int = 150


class GenerateStudyNotes(BaseModel):
    job_name: str
    max_tokens: int = 150


class FactualAnswers(BaseModel):
    question: str
    max_tokens: int = 60


class GrammarCorrection(BaseModel):
    text: str
    max_tokens: int = 60


class AdTextGeneration(BaseModel):
    job_name: str
    job_description: str
    advertise_location: str
    intended_audience: str
    max_tokens: int = 100


class CoverLetterHelp(BaseModel):
    job_name: str
    job_description: str
    company_name: str
    max_tokens: int = 100


class ResumeHelp(BaseModel):
    job_name: str
    job_description: str
    max_tokens: int = 100
