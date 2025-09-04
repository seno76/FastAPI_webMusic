import hashlib
from src.models.modelsORM import *
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, func, delete
from typing import Optional, List
from src.bd.database import session_factory
from src.schemas import UserPD, UserPDData, PlayListPDData
from src.utils.abstractions import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):

    model = User

    def _get_users_with_filter(self, filter_condition=None) -> List[UserPDData]:
        with session_factory() as session:
            query = select(self.model)
            if filter_condition:
                query = query.where(filter_condition)

            users = session.execute(query).scalars().all()
            return [UserPDData.model_validate(user) for user in users]

    def find_all(self) -> UserPD:
        return self._get_users_with_filter()

    def get_by_id(self, user_id: int) -> UserPDData:
        with session_factory() as session:

            query = (
                select(self.model)
                .where(self.model.id == user_id)
                .options(
                    selectinload(self.model.author),
                    selectinload(self.model.playlists),
                )
            )
            user = session.execute(query).scalar_one()
            return UserPDData.model_validate(user)

    def is_active(self) -> List[UserPDData]:
        return self._get_users_with_filter(self.model.is_active == True)

    def is_passive(self) -> List[UserPDData]:
        return self._get_users_with_filter(self.model.is_active == False)

    def by_username(self, user_name: str) -> Optional[UserPDData]:
        with session_factory() as session:
            query = select(self.model).where(self.model.username == user_name)
            user = session.execute(query).scalar_one_or_none()
            if user is None:
                return None
            return UserPDData.model_validate(user)

    # ORM (Поиск пользователя по мылу)
    def user_by_email(self, email: str) -> Optional[UserPDData]:
        with session_factory() as session:
            query = select(self.model).where(self.model.email == email)
            user = session.execute(query).scalar_one_or_none()
            if user is None:
                return None
            return UserPDData.model_validate(user)

    # ORM (Установление значения статуса)
    def set_user_status(self, user_id: int, status: bool) -> Optional[UserPDData]:
        with session_factory() as session:
            user = session.get(self.model, user_id)
            query = (
                update(self.model)
                .where(self.model.id == user_id)
                .values(is_active=status)
            )
            session.execute(query)
            session.commit()
            return UserPDData.model_validate(user)

    # Вывод количества пользователей (user) в бд
    def count_users(self, only_active: bool = None) -> int:
        with session_factory() as session:
            query = select(func.count(self.model.id))
            if only_active:
                query = query.where(self.model.is_active == True)
            elif only_active is False:
                query = query.where(self.model.is_active == False)
            res = session.execute(query).scalar()
        return res

    # Создание нового пользователя
    def create_user(self, data: dict) -> Optional[UserPDData]:
        with session_factory() as session:
            user = self.model(**data)
            password = user.password_hash.encode("utf-8")
            user.password_hash = hashlib.sha256(password).hexdigest()
            session.add(user)
            session.commit()
            return UserPDData.model_validate(user)

    def delete_user_by_id(self, id_user: int) -> None:
        with session_factory() as session:
            query = delete(self.model).where(self.model.id == id_user)
            session.execute(query)
            session.commit()
            return None

    # Возвращение плей листа + музыки в ней
    def get_plalylist_by_user_id(self, user_id: int) -> List[PlayListPDData]:
        with session_factory() as session:
            query = select(self.model).where(self.model.id == user_id)
            user = session.execute(query).scalar()
            return [
                PlayListPDData.model_validate(playlist) for playlist in user.playlists
            ]

    def auth_user(self, username: str, password: str) -> int:
        with session_factory() as session:
            qeury = select(self.model).filter(self.model.username == username)
            user = session.execute(qeury).scalar_one_or_none()
            return user and user.password_hash == password
