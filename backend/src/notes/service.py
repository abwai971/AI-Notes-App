from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import NoteCreateModel, NoteUpdateModel
from src.db.models import Note, Folder
from sqlmodel import select, desc


class NoteService:
    async def _get_user_folder(
        self,
        folder_uid: str,
        user_uid: str,
        session: AsyncSession,
    ) -> Folder | None:
        statement = select(Folder).where(
            Folder.uid == folder_uid,
            Folder.user_uid == user_uid,
        )

        result = await session.exec(statement)
        return result.first()
    
    async def get_all_notes(self, user_uid: str, folder_uid: str | None,  session:AsyncSession):
        statement = select(Note).where(
            Note.user_uid == user_uid,
            Note.is_archived.is_(False),
        )
        if folder_uid is not None:
            statement = statement.where(Note.folder_uid == folder_uid)

        statement = statement.order_by(desc(Note.updated_at))
        result = await session.exec(statement)
        return result.all()

    async def create_note(self, note_data: NoteCreateModel, user_uid: str, session: AsyncSession):
        note_data_dict = note_data.model_dump()
        if note_data.folder_uid is not None:
            folder = await self._get_user_folder(
                note_data.folder_uid,
                user_uid,
                session,
            )

            if folder is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Folder not found.",
                )
        new_note = Note(**note_data_dict)
        new_note.user_uid = user_uid
        session.add(new_note)
        await session.commit()
        await session.refresh(new_note)
        return new_note
    
    async def get_note(self, user_uid: str, note_uid: str, session: AsyncSession):
        statement = select(Note).where(Note.uid == note_uid,Note.user_uid == user_uid)
        result = await session.exec(statement)
        note = result.first()
        return note if note is not None else None    

    async def update_note(self, user_uid: str, note_uid: str, update_data: NoteUpdateModel, session: AsyncSession):
        note_to_update = await self.get_note(user_uid, note_uid, session)
        if note_to_update is None:
            return None
        update_data_dict = update_data.model_dump(exclude_unset=True)
        folder_uid = update_data_dict.get("folder_uid")
        if folder_uid is not None:
            folder = await self._get_user_folder(
                    folder_uid,
                    user_uid,
                    session,
                )

            if folder is None:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Folder not found.",
                    )
        if (
            ("title" in update_data_dict and update_data_dict["title"] != note_to_update.title)
            or
            ("content" in update_data_dict and update_data_dict["content"] != note_to_update.content)
        ):
            note_to_update.summary = None
            note_to_update.tags = None
            note_to_update.ai_updated_at = None
        for k, v in update_data_dict.items():
            setattr(note_to_update, k, v)
        await session.commit()
        await session.refresh(note_to_update)
        return note_to_update
    
    async def delete_note(self,user_uid: str, note_uid: str, session: AsyncSession):
        note_to_delete = await self.get_note(user_uid, note_uid, session)
        if note_to_delete is None:
            return None
        await session.delete(note_to_delete)
        await session.commit()
        return 
    
