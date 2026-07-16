from src.db.models import User
from .schemas import UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.core.utils import generate_password_hash

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user
    
    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)

        return user is not None
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        email=user_data.email,
        password_hash=generate_password_hash(user_data.password),
        )

        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)

        return new_user
    
    async def update_user(self, user:User, user_data: dict, session: AsyncSession):
        for k, v in user_data.items():
            setattr(user, k, v)
        
        await session.commit()

        return user
    




