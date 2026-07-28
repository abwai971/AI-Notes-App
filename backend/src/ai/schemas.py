from pydantic import BaseModel

class SummaryResponse(BaseModel):
    summary: str


class TagsResponse(BaseModel):
    tags: list[str]

class QuestionResponse(BaseModel):
    answer: str

class QuestionRequest(BaseModel):
    question: str
