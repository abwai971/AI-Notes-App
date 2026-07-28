from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import SummaryResponse, TagsResponse, QuestionResponse, QuestionRequest
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer
from src.notes.service import NoteService
from .service import AIService

ai_router = APIRouter()
access_token_bearer = AccessTokenBearer()
note_service = NoteService()
ai_service = AIService()

@ai_router.post("/notes/{note_uid}/summary", response_model=SummaryResponse, status_code=status.HTTP_200_OK)
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
