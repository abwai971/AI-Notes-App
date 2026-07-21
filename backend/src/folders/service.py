from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import createFolderModel, updateFolderModel
from src.db.models import Folder
from sqlmodel import select, desc


class folderService:
    async def get_all_folders(self, user_uid: str,  session=AsyncSession):
        statement = select(Folder).where(Folder.user_uid == user_uid).order_by(desc(Folder.created_at))
        result = await session.exec(statement)
        return result.all()

    async def create_folder(self, folder_data: createFolderModel, user_uid: str, session: AsyncSession):
        folder_data_dict = folder_data.model_dump()
        new_folder = Folder(**folder_data_dict)
        new_folder.user_uid = user_uid
        session.add(new_folder)
        await session.commit()
        await session.refresh(new_folder)
        return new_folder
    
    async def get_folder(self, user_uid: str, folder_uid: str, session: AsyncSession):
        statement = select(Folder).where(Folder.uid == folder_uid,Folder.user_uid == user_uid)
        result = await session.exec(statement)
        folder = result.first()
        return folder if folder is not None else None    

    async def update_folder(self, user_uid: str, folder_uid: str, update_data: updateFolderModel, session: AsyncSession):
        folder_to_update = await self.get_folder(user_uid, folder_uid, session)
        if folder_to_update is None:
            return None
        update_data_dict = update_data.model_dump(exclude_unset=True)
        for k, v in update_data_dict.items():
            setattr(folder_to_update, k, v)
        await session.commit()
        await session.refresh(folder_to_update)
        return folder_to_update
    
    async def delete_folder(self,user_uid: str, folder_uid: str, session: AsyncSession):
        folder_to_delete = await self.get_folder(user_uid, folder_uid, session)
        if folder_to_delete is None:
            return None
        await session.delete(folder_to_delete)
        await session.commit()
        return 
    