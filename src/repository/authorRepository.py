from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete, update
from typing import Optional, List
from src.models.modelsORM import *
from src.schemas.author import *
from src.bd.database import session_factory
from src.utils.abstractions import SQLAlchemyRepository

class AuthorRepository(SQLAlchemyRepository):
    model = Author

    def get_by_id(self, author_id: int) -> Optional[AuthorPDData]:
        with session_factory() as session:
            query = (
                select(self.model)
                .where(self.model.id == author_id)
                .options(
                    selectinload(self.model.user),
                    selectinload(self.model.tracks),
                )
            )
            author = session.execute(query).scalar_one_or_none()
            if author is None:
                return None
            return AuthorPDData.model_validate(author)

    def get_by_user_id(self, user_id: int) -> Optional[AuthorPDData]:
        with session_factory() as session:
            query = select(self.model).where(self.model.id_user == user_id)
            author = session.execute(query).scalar_one_or_none()
            if author is None:
                return None
            return AuthorPDData.model_validate(author)

    def create(self, data: AuthorCreate) -> AuthorPDData:
        with session_factory() as session:
            # Проверка существования пользователя
            user_exists = session.scalar(
                select(User.id).where(User.id == data.id_user)
            )
            if not user_exists:
                raise ValueError(f"Пользователя с id {data.id_user} не существует в базе данных")

            # Проверка существования автора с таким user_id
            author_exists = session.scalar(
                select(self.model.id).where(self.model.id_user == data.id_user)
            )
            if author_exists:
                raise ValueError(f"Уже существует автор с таким user_id {data.id_user}")

            author = self.model(**data.model_dump())
            session.add(author)
            session.commit()
            session.refresh(author)
            return AuthorPDData.model_validate(author)

    def delete_by_id(self, author_id: int) -> None:
        with session_factory() as session:
            query = delete(self.model).where(self.model.id == author_id)
            session.execute(query)
            session.commit()

    def update(self, author_id: int, data: AuthorUpdate) -> Optional[AuthorPDData]:
        with session_factory() as session:
            author = session.get(self.model, author_id)
            if author is None:
                return None
            
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(author, field, value)
            
            session.commit()
            session.refresh(author)
            return AuthorPDData.model_validate(author)

    def find_all(self, offset: int = 0, limit: int = 100) -> List[AuthorPDData]:
        with session_factory() as session:
            query = (
                select(self.model)
                .offset(offset)
                .limit(limit)
                .options(
                    selectinload(self.model.user),
                    selectinload(self.model.tracks)
                )
            )
            authors = session.execute(query).scalars().all()
            return [AuthorPDData.model_validate(author) for author in authors]
