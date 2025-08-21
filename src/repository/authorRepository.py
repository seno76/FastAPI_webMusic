from sqlalchemy.orm import Session, lazyload
from typing import Optional, List
from src.models.modelsORM import *
from sqlalchemy import select, delete, update
from src.models.modelsPD import *


# Получение автора по id
def get_author_by_id(db: Session, author_id: int) -> Optional[AuthorPDData]:
    with db() as session:
        query = select(Author)\
            .options(
                lazyload(Author.user),
                lazyload(Author.tracks),
            ).where(Author.id == author_id)
        author = session.execute(query).scalar_one_or_none()
        if author is None:
            return None
        return AuthorPDData.model_validate(author)


# Получение по пользователю автора
def get_by_user_id(db: Session, user_id: int) -> Optional[AuthorPDData]:
    with db() as session:
        query = select(Author).where(Author.id_user == user_id)
        author = session.execute(query).scalar_one_or_none()
        if author is None:
            return None
        return AuthorPDData.model_validate(author)


# Создание нового автора
def create_new_author(db: Session, data: AuthorCreate) -> AuthorPDData:
    """Создает нового автора с проверкой существования пользователя"""
    with db() as session:
        user_exists = session.scalar(
            select(User.id).where(User.id == data.id_user)
        )
        if not user_exists:
            raise ValueError(f"Пользователя с id {data.id_user} не существует в базе данных")

        author_exists = session.scalar(
            select(Author.id).where(Author.id_user == data.id_user)
        )
        if author_exists:
            raise ValueError(f"Уже существует автор с таким user_id {data.id_user}")

        author = Author(**data.model_dump())
        session.add(author)
        session.commit()
        session.refresh(author)
        return AuthorPDData.model_validate(author)


def delete_aythor_by_id(db: Session, author_id: int) -> None:
    with db() as session:
        query = delete(Author).where(Author.id == author_id)
        session.execute(query)
        session.commit()


# Обновление данных автора
def update_author(db: Session, author_id: int, data: AuthorUpdate) -> Optional[AuthorPDData]:
    with db() as session:
        author = session.execute(select(Author).where(Author.id == author_id)).scalar_one_or_none()
        if author is None:
            return None
        query = update(Author).where(Author.id == author_id).values(**data.model_dump(exclude_unset=True))
        session.execute(query)
        session.commit()
        session.refresh(author)
        return AuthorPDData.model_validate(author)




# Получение всех авторов
def get_all_authors(db: Session, offset: int = 0, limit: int = 100) -> List[AuthorPDData]:
    with db() as session:
        query = select(Author).offset(offset).limit(limit).options(lazyload(Author.user), lazyload(Author.tracks))
        authors = session.execute(query).scalars().all()
        return [AuthorPDData.model_validate(author) for author in authors]

print(dir())