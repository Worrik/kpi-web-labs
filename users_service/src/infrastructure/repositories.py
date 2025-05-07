from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from src.application.interfaces import UserRepo
from src.domain.entities import UserDM
from src.exceptions.database_exceptions import IntegrityError
from src.infrastructure.models import UserModel


class UserRepoImpl(UserRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    def model_to_entity(self, user: UserModel) -> UserDM:
        return UserDM(
            id=user.id,
            created_at=user.created_at,
            name=user.name,
            email=user.email,
        )

    async def create(
        self,
        name: str,
        email: str,
    ) -> UserDM:
        user = UserModel(
            name=name,
            email=email,
        )
        self.db_session.add(user)
        try:
            await self.db_session.commit()
        except sa.exc.IntegrityError:
            await self.db_session.rollback()
            raise IntegrityError
        return self.model_to_entity(user)

    async def get_by_email(self, email: str) -> UserDM | None:
        query = sa.select(UserModel).where(UserModel.email == email).limit(1)
        result = await self.db_session.execute(query)
        user = result.scalars().first()
        return self.model_to_entity(user) if user else None
