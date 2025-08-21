from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from pydantic import AnyUrl
from src.models.modelsORM import *
from sqlalchemy import select, delete, insert
from src.models.modelsPD import (
    PlayListBase,
    PlayListUpdate,
    PlayListCreate,
    PlayListPD,
    PlayListPDData,
    TrackPD
)


def create_playlist(db: Session, data: PlayListCreate) -> PlayListPD:
    with db() as session:
        playlist = PlayList(**data.model_dump())
        playlist.cover_url = str(playlist.cover_url)
        session.add(playlist)
        session.commit()
        session.refresh(playlist)
        return PlayListPD.model_validate(playlist)


def delete_playlist(db: Session, playlist_id: int) -> bool:
    with db() as session:
        playlist = session.scalar(select(PlayList).where(PlayList.id == playlist_id))
        if not playlist:
            return False

        session.delete(playlist)
        session.commit()
        return True


def add_track_to_playlist(db: Session, playlist_id: int, track_id: int, order: int) -> None | PlayListPDData:
    with db() as session:
        # Проверяем существование плейлиста и трека
        if not (session.scalar(select(PlayList.id).where(PlayList.id == playlist_id)) and
                session.scalar(select(Track.id).where(Track.id == track_id))):
            return False

        # Добавляем связь
        session.execute(insert(PlaylistTrack)
            .values(playlist_id=playlist_id, track_id=track_id, order=order)
        )
        session.commit()
        playlist = session.get(PlayList, playlist_id)
        return PlayListPDData.model_validate(playlist)

def get_playlists(db: Session, limit: int = 1000, offset: int = 0) -> List[PlayListPD]:
    with db() as session:
        query = select(PlayList).limit(limit).offset(offset)
        playlists = session.execute(query).scalars().all()
        return [PlayListPD.model_validate(playlist) for playlist in playlists]

def get_playlist_by_id(db: Session, id_playlist: int) -> PlayListPDData | None:
    with db() as session:
        playlist = session.get(PlayList, id_playlist)
        if not playlist:
            return None
        return PlayListPDData.model_validate(playlist)

def update_by_id(db: Session, id_playlist: int, data: PlayListUpdate) -> PlayListPDData | None:
    with db() as session:
        stmt = select(PlayList).where(PlayList.id == id_playlist)
        playlist = session.execute(stmt).scalar_one_or_none()
        if not playlist:
            return None

        data.cover_url = str(data.cover_url)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(playlist, field, value)

        session.commit()
        session.refresh(playlist)

        return PlayListPDData.model_validate(playlist)

def get_tracks_by_playlist(db: Session, id_playlist: int) -> List[TrackPD] | None:
    with db() as session:
        query = select(PlayList).where(PlayList.id == id_playlist)
        playlist = session.execute(query).scalar_one_or_none()
        if not playlist:
            return None
        session.commit()
        return [TrackPD.model_validate(track) for track in playlist.tracks]