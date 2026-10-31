from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import SummaryResponse, TagsResponse, QuestionRequest, QuestionResponse, SummaryTaskResponse
from .provider import gemini_provider
from .prompts import SUMMARY_PROMPT, TAG_PROMPT, QUESTION_PROMPT
from src.notes.service import NoteService
from  datetime import datetime, timezone
import json
from src.celery_task import generate_summary_task

class AIService:
    def __init__(self):
        self.note_service = NoteService()

    async def summarize_note(self,user_uid: str, note_uid: str, session: AsyncSession):
        note = await self.note_service.get_note(user_uid, note_uid, session)

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        if note.summary:
            return SummaryTaskResponse(
            task_id="",
            status="SUCCESS",
            summary=note.summary,
        )

        task = generate_summary_task.delay(
        str(user_uid),
        str(note_uid),
        )

        return SummaryTaskResponse(
            task_id=task.id,
            status="PENDING",
            summary=None,
        )

    async def generate_tags(self, user_uid: str, note_uid: str, session: AsyncSession):
        note = await self.note_service.get_note(user_uid, note_uid, session)
        # note.tags = None
        # print("tags:", note.tags, flush=True)
        # print("type:", type(note.tags), flush=True)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        if note.tags:
            return TagsResponse(tags=note.tags)

        full_content = f"""
                Title:
                {note.title}
                Content:
                {note.content}
                """

        prompt = TAG_PROMPT.format(note_content=full_content)

        generated_tags = await gemini_provider.generate(prompt)

        tags = json.loads(generated_tags)

        note.tags = tags

        note.ai_updated_at = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(note)

        return TagsResponse(tags=note.tags)

    async def ask_questions(self, user_uid: str, note_uid: str, request_body: QuestionRequest, session: AsyncSession):
        note = await self.note_service.get_note(user_uid, note_uid, session)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        full_content = f"""
                     Title:
                     {note.title}
                     Content:
                     {note.content}
                     """

        prompt = QUESTION_PROMPT.format(note_content=full_content, user_question=request_body.question)
        answer = await gemini_provider.generate(prompt)

        return QuestionResponse(answer=answer)

        
        

        
        

