from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import NoteCreateModel, NoteUpdateModel, Note, NoteSummary
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer
from .service import NoteService
from .schemas import SemanticSearchRequest

note_router = APIRouter()
access_token_bearer = AccessTokenBearer()
note_service = NoteService()

#create note
@note_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Note)
async def create_note(note_data: NoteCreateModel, 
                        session: AsyncSession = Depends(get_session), 
                        token_details: dict = Depends(access_token_bearer)):
    user_id = token_details.get('user')['user_uid']
    new_note = await note_service.create_note(note_data, user_id, session)
    return new_note

#get_all_notes
@note_router.get("/", response_model=list[NoteSummary])
async def get_all_notes(folder_uid: str | None = None, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    user_uid = token_details["user"]["user_uid"]
    notes = await note_service.get_all_notes(user_uid, folder_uid, session)
    return notes

#get_note_by_id
@note_router.get("/{note_uid}", response_model=Note)
async def get_note(note_uid: str, 
                     token_details: dict = Depends(access_token_bearer),
                   session: AsyncSession = Depends(get_session), 
                   ) -> dict:
    user_uid = token_details["user"]["user_uid"]
    note = await note_service.get_note(user_uid, note_uid, session)
    if note:
        return note
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
#update_note
@note_router.patch("/{note_uid}", response_model=Note)
async def update_note(note_uid: str,
                        note_update_data: NoteUpdateModel,
                        token_details: dict = Depends(access_token_bearer),
                        session: AsyncSession = Depends(get_session)) -> dict:
    user_uid = token_details["user"]["user_uid"]
    updated_note = await note_service.update_note(user_uid, note_uid, note_update_data, session)
    if updated_note:
        return updated_note
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

#delete_note
@note_router.delete("/{note_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_uid: str, 
                      token_details: dict = Depends(access_token_bearer),
                      session: AsyncSession = Depends(get_session), 
                      ) -> None:
    user_uid = token_details["user"]["user_uid"]
    note_to_delete = await note_service.delete_note(user_uid, note_uid, session)
    if note_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    else:
        return 

#semantic search 
@note_router.post("/search/semantic", response_model=list[Note])
async def semantic_search_notes(search_data: SemanticSearchRequest, 
                                session: AsyncSession = Depends(get_session), 
                                token_data: dict = Depends(access_token_bearer),):
    notes = await note_service.semantic_search(
        user_uid=token_data["user"]["user_uid"],
        query=search_data.query,
        session=session,
        limit=search_data.limit,
    )
    return notes



