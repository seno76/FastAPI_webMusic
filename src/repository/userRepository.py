from src.models.modelsORM import *
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, text, Engine, update, func, delete, Result
from src.models.modelsPD import *
from typing import Optional, List


# CORE (Поиск пользователя по id)
def get_user_by_id_core(engine: Engine, user_id: int) -> User:
    with engine.connect() as conn:
        query = text("SELECT * FROM users WHERE id=:id")
        query = query.bindparams(id=user_id)
        user = conn.execute(query).all()
        conn.commit()
        return user


# ORM (Поиск пользователя по id)
def get_user_by_id_orm(session: Session, user_id: int) -> UserPDData:
    with session() as session:
        query = (select(User).where(User.id == user_id)
             .options(
                selectinload(User.author),
                selectinload(User.playlists),
            )
        )
        user = session.execute(query).scalars().first()
        session.commit()
        UserPDData.model_validate(user)
        return UserPDData.model_validate(user)


# ORM (Поиск пользователя по статусу активации)
def get_users_is_active(session: Session) -> List[UserPDData]:
    with session() as session:
        query = select(User).where(User.is_active == True)
        users = session.execute(query).scalars().all()
        return [UserPDData.model_validate(user) for user in users]


# ORM (Поиск пользователя по имени)
def get_user_by_username(session: Session, user_name: str) -> Optional[UserPDData]:
    with session() as session:
        query = select(User).where(User.username == user_name)
        user = session.execute(query).scalar_one_or_none()
        if user is None:
            return None
        return UserPDData.model_validate(user)


# ORM (Поиск пользователя по мылу)
def get_user_by_email(session: Session, email: str) -> Optional[UserPDData]:
    with session() as session:
        query = select(User).where(User.email == email)
        user = session.execute(query).scalar_one_or_none()
        if user is None:
            return None
        return UserPDData.model_validate(user)


# ORM (Установление значения статуса)
def set_user_status(db: Session, user_id: int, status: bool) -> Optional[UserPDData]:
    with db() as session:
        query = update(User).where(User.id == user_id).values(is_active=status)
        session.execute(query)
        session.commit()
        return get_user_by_id_orm(db, user_id)


# Вывод количества пользователей (user) в бд
def get_count_users(db: Session, only_active: bool = None) -> int:
    with db() as session:
        query = select(func.count(User.id))
        if only_active:
            query = query.where(User.is_active == True)
        elif only_active is False:
            query = query.where(User.is_active == False)
        res = session.execute(query).scalar()
    return res


# Создание нового пользователя
def create_user(db: Session, data: dict) -> Optional[UserPDData]:
    with db() as session:
        user = User(**data)
        session.add(user)
        session.commit()
        return UserPDData.model_validate(user)

def delete_user_by_id(db: Session, id_user: int) -> None:
    with db() as session:
        query = delete(User).where(User.id == id_user)
        session.execute(query)
        session.commit()


# Возвращение плей листа + музыки в ней
def get_plalylist_by_user_id(db: Session, user_id: int) -> List[PlayListPDData]:
    with db() as session:
        query = select(PlayList).where(PlayList.id_user == user_id)
        playlists = session.execute(query).unique().scalars().all()
        return [PlayListPDData.model_validate(playlist) for playlist in playlists]