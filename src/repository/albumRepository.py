import datetime

from sqlalchemy.orm import Session, joinedload
from typing import Optional, List, Dict
from src.models.modelsORM import *
from sqlalchemy import select, delete, update
from src.models.modelsPD import AlbumPD, AlbumPDData, AlbumCreate, AlbumUpdate


# Получение альбома по ID
def get_album_by_id(db: Session, album_id: int) -> Optional[AlbumPDData]:
    with db() as session:
        album = session.scalar(
            select(Album)
            .options(joinedload(Album.tracks), joinedload(Album.genre), joinedload(Album.userPreference))
            .where(Album.id == album_id)
        )
        if not album:
            return None
        return AlbumPDData.model_validate(album)

def get_all_albums(db: Session, limit: int, offset: int) -> Optional[AlbumPDData]:
    with db() as session:
        albums = session.execute(select(Album).limit(limit).offset(offset)).scalars().all()
        return [AlbumPDData.model_validate(album) for album in albums]


# Создание ноовго альбома
def create_album(db: Session, data: AlbumCreate) -> AlbumPD:
    with db() as session:
        album = Album(**data.model_dump(), created_at=datetime.datetime.now()) # <------------------- нужно потом когда буду переписывать миграции сделать чтобы данные в схеме sql автоматически генерировались
        album.cover_url = str(album.cover_url)
        session.add(album)
        session.commit()
        session.refresh(album)
        return AlbumPD.model_validate(album)


# Удаляем альбом путем мягкой связи
def delete_album_by_id(db: Session, album_id: int) -> bool:
    with db() as session:
        album = session.scalar(select(Album).where(Album.id == album_id))
        if not album:
            return False

        session.execute(update(Track).where(Track.album_id == album_id).values(album_id=None))
        session.delete(album)
        session.commit()
        return True

# Получение альбомов по жанру
def get_albums_by_genre(db: Session, genre_id: int, limit: int = 1000, offset: int = 0) -> List[AlbumPDData]:
    with db() as session:
        albums = session.scalars(select(Album).where(Album.genre_id == genre_id).limit(limit).offset(offset)).all()
        return [AlbumPDData.model_validate(a) for a in albums]


def update_album(db: Session, album_id: int, data: AlbumUpdate) -> Optional[AlbumPD]:
    with db() as session:
        if not session.get(Album, album_id):
            return None

        session.execute(
            update(Album)
            .where(Album.id == album_id)
            .values(**data.model_dump(exclude_unset=True))
        )
        session.commit()

        updated_album = session.get(Album, album_id)
        return AlbumPD.model_validate(updated_album)