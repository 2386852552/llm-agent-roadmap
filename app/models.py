from pydantic import BaseModel

class SummaryResult(BaseModel):
    title: str
    summary: str
    keywords: list[str]
    questions: list[str]