from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import Folder, createFolderModel, updateFolderModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer
from .service import folderService


folder_router = APIRouter()
access_token_bearer = AccessTokenBearer()
folder_service = folderService()

#create folder
@folder_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Folder)
async def create_folder(folder_data: createFolderModel, 
                        session: AsyncSession = Depends(get_session), 
                        token_details: dict = Depends(access_token_bearer)):
    user_id = token_details.get('user')['user_uid']
    new_folder = await folder_service.create_folder(folder_data, user_id, session)
    return new_folder

#get_all_folders
@folder_router.get("/", response_model=list[Folder])
async def get_all_folders(session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    user_uid = token_details["user"]["user_uid"]
    folders = await folder_service.get_all_folders(user_uid, session)
    return folders

#get_folder_by_id
@folder_router.get("/{folder_uid}", response_model=Folder)
async def get_folder(folder_uid: str, 
                     token_details: dict = Depends(access_token_bearer),
                   session: AsyncSession = Depends(get_session), 
                   ) -> dict:
    user_uid = token_details["user"]["user_uid"]
    folder = await folder_service.get_folder(user_uid, folder_uid, session)
    if folder:
        return folder
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    
#update_folder
@folder_router.patch("/{folder_uid}", response_model=Folder)
async def update_folder(folder_uid: str,
                        folder_update_data: updateFolderModel,
                        token_details: dict = Depends(access_token_bearer),
                        session: AsyncSession = Depends(get_session)) -> dict:
    user_uid = token_details["user"]["user_uid"]
    updated_folder = await folder_service.update_folder(user_uid, folder_uid, folder_update_data, session)
    if updated_folder:
        return updated_folder
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")

#delete_folder
@folder_router.delete("/{folder_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(folder_uid: str, 
                      token_details: dict = Depends(access_token_bearer),
                      session: AsyncSession = Depends(get_session), 
                      ) -> None:
    user_uid = token_details["user"]["user_uid"]
    folder_to_delete = await folder_service.delete_folder(user_uid, folder_uid, session)
    if folder_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found")
    else:
        return {}



