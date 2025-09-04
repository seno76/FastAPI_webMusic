import datetime

from sqlalchemy.orm import Session, joinedload
from typing import Optional, List, Dict
from src.models.modelsORM import *
from sqlalchemy import select, delete, update
from src.schemas.album import AlbumPD, AlbumPDData, AlbumCreate, AlbumUpdate
from src.utils.abstractions import AbstractRepository, SQLAlchemyRepository
from src.bd.database import session_factory


class AlbumRepository(SQLAlchemyRepository):

    model = Album

    # Получение альбома по ID
    def get_album_by_id(self, album_id: int) -> Optional[AlbumPDData]:
        with session_factory() as session:
            album = session.scalar(
                select(self.model)
                .options(
                    joinedload(self.model.tracks),
                    joinedload(self.model.genre),
                    joinedload(self.model.user_preferences),
                )
                .where(self.model.id == album_id)
            )
            if not album:
                return None
            return AlbumPDData.model_validate(album)

    def get_all_albums(self, limit: int, offset: int) -> Optional[AlbumPDData]:
        with session_factory() as session:
            albums = (
                session.execute(select(self.model).limit(limit).offset(offset))
                .scalars()
                .all()
            )
            return [AlbumPDData.model_validate(album) for album in albums]

    # Создание ноовго альбома
    def create_album(self, data: AlbumCreate) -> AlbumPD:
        with session_factory() as session:
            album_dict = data.model_dump()
            album = Album(
                **album_dict, created_at=datetime.datetime.now()
            )  # <------------------- нужно потом когда буду переписывать миграции сделать чтобы данные в схеме sql автоматически генерировались
            album.cover_url = str(album.cover_url)
            session.add(album)
            session.commit()
            session.refresh(album)
            return AlbumPD.model_validate(album)

    # Удаляем альбом путем мягкой связи
    def delete_album_by_id(self, album_id: int) -> bool:
        with session_factory() as session:
            album = session.scalar(select(self.model).where(self.model.id == album_id))
            if not album:
                return False

            session.execute(
                update(Track).where(Track.album_id == album_id).values(album_id=None)
            )
            session.delete(album)
            session.commit()
            return True

    # Получение альбомов по жанру
    def get_albums_by_genre(
        self, genre_id: int, limit: int = 1000, offset: int = 0
    ) -> List[AlbumPDData]:
        with session_factory() as session:
            albums = session.scalars(
                select(self.model)
                .where(self.model.genre_id == genre_id)
                .limit(limit)
                .offset(offset)
            ).all()
            return [AlbumPDData.model_validate(a) for a in albums]

    def update_album(self, album_id: int, data: AlbumUpdate) -> Optional[AlbumPD]:
        with session_factory() as session:
            if not session.get(self.model, album_id):
                return None

            data.cover_url = str(data.cover_url)

            session.execute(
                update(self.model)
                .where(self.model.id == album_id)
                .values(**data.model_dump(exclude_unset=True))
            )
            session.commit()

            updated_album = session.get(self.model, album_id)
            return AlbumPD.model_validate(updated_album)
