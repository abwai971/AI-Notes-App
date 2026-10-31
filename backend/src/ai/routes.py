from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import SummaryResponse, TagsResponse, QuestionResponse, QuestionRequest
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer
from src.notes.service import NoteService
from .service import AIService
from celery.result import AsyncResult
from src.celery_task import generate_summary_task
from .schemas import SummaryTaskResponse, TaskStatusResponse
from celery.result import AsyncResult
from src.celery_task import c_app

ai_router = APIRouter()
access_token_bearer = AccessTokenBearer()
note_service = NoteService()
ai_service = AIService()

@ai_router.post("/notes/{note_uid}/summary", response_model=SummaryTaskResponse, status_code=status.HTTP_200_OK)
async def generate_summary(note_uid: str, session: AsyncSession = Depends(get_session), 
                           token_data: dict = Depends(access_token_bearer)):
    
    return await ai_service.summarize_note(user_uid=token_data["user"]["user_uid"], note_uid=note_uid, session=session)

@ai_router.post("/notes/{note_uid}/tags", response_model=TagsResponse, status_code=status.HTTP_200_OK)
async def generate_tag(note_uid: str, session: AsyncSession = Depends(get_session),
                        token_data: dict = Depends(access_token_bearer)):

    return await ai_service.generate_tags(user_uid=token_data["user"]["user_uid"], note_uid=note_uid, session=session)

@ai_router.post("/notes/{note_uid}/questions", response_model=QuestionResponse, status_code=status.HTTP_200_OK)
async def generate_qna(note_uid: str, body: QuestionRequest, 
                       session: AsyncSession = Depends(get_session), 
                        token_data: dict = Depends(access_token_bearer)):
    return await ai_service.ask_questions(user_uid=token_data["user"]["user_uid"], note_uid=note_uid, request_body=body, session=session)


@ai_router.get("/notes/{note_uid}/summary/tasks/{task_id}",response_model=SummaryTaskResponse,status_code=status.HTTP_200_OK,)
async def get_summary_task_status(
    note_uid: str,
    task_id: str,
    session: AsyncSession = Depends(get_session),
    token_data: dict = Depends(access_token_bearer),
):
    user_uid = token_data["user"]["user_uid"]

    # Verify that the note belongs to this user.
    note = await note_service.get_note(user_uid, note_uid, session)

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    # Check the Celery task status using Redis.
    task_result = AsyncResult(task_id, app=c_app)
    task_status = task_result.status

    if task_status == "SUCCESS":
        result = task_result.result

        # Ensure this task generated a summary for the requested note.
        if not isinstance(result, dict) or result.get("note_uid") != str(note.uid):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Summary task not found for this note",
            )

        return SummaryTaskResponse(
            task_id=task_id,
            status="SUCCESS",
            summary=result["summary"],
        )

    if task_status == "FAILURE":
        return SummaryTaskResponse(
            task_id=task_id,
            status="FAILURE",
            summary=None,
        )

    return SummaryTaskResponse(
        task_id=task_id,
        status=task_status,
        summary=None,
    )

