from pydantic import BaseModel

class SummaryResponse(BaseModel):
    summary: str


class TagsResponse(BaseModel):
    tags: list[str]

class QuestionResponse(BaseModel):
    answer: str

class QuestionRequest(BaseModel):
    question: str

class SummaryTaskResponse(BaseModel):
    task_id: str
    status: str
    summary: str | None = None


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    summary: str | None = None
    error: str | None = None