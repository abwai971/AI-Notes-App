
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config
from src.notes.service import NoteService
from src.ai.provider import gemini_provider
from src.ai.prompts import SUMMARY_PROMPT


worker_engine = create_async_engine(
    Config.DATABASE_URL,
    pool_pre_ping=True,
    poolclass=NullPool,
)

worker_session = async_sessionmaker(
    bind=worker_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def generate_summary(
    user_uid: str,
    note_uid: str,
) -> dict:
    async with worker_session() as session:
        note_service = NoteService()

        note = await note_service.get_note(
            user_uid,
            note_uid,
            session,
        )

        if not note:
            raise ValueError("Note not found")

        if note.summary:
            return {
                "note_uid": str(note.uid),
                "summary": note.summary,
            }

        full_content = f"""
                    Title:
                    {note.title}

                    Content:
                    {note.content}
                    """

        prompt = SUMMARY_PROMPT.format(
            note_content=full_content,
        )

        summary = await gemini_provider.generate(prompt)

        note.summary = summary
        note.ai_updated_at = datetime.now(timezone.utc)

        await session.commit()

        return {
            "note_uid": str(note.uid),
            "summary": summary,
        }
