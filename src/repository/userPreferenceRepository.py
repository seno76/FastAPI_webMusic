from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from src.bd.database import session_factory
from typing import List, Optional, Dict
from src.models.modelsORM import *
from src.models.modelsPD import (
    PreferenceAlbum,
    PreferenceAlbumPD,
    PreferenceAlbumPDData,
    PreferenceTrack,
    PreferenceTrackPD,
    PreferenceTrackPDData,
    Preference,
    TrackPD,
    AlbumPD
)

def get_all_tracks_preference(db: Session, limit: int = 1000, offset: int = 0) -> List[PreferenceTrackPD]:
    with db() as session_factory:
        query = select(UserTrackPreference).limit(limit).offset(offset)
        pr_tracks = session_factory.execute(query).scalars().all()
        return [PreferenceTrackPD.model_validate(track) for track in pr_tracks]

def get_all_albums_preference(db: Session, limit: int = 1000, offset: int = 0) -> List[PreferenceAlbumPD]:
    with db() as session_factory:
        query = select(UserAlbumPreference).limit(limit).offset(offset)
        pr_albums = session_factory.execute(query).scalars().all()
        return [PreferenceAlbumPD.model_validate(album) for album in pr_albums]

def get_preference_track_for_user(db: Session, id_user: int) -> List[TrackPD]:
    with db() as session:
        query = select(UserTrackPreference).where(UserTrackPreference.user_id == id_user)
        result = session.execute(query).scalars().all()
        return [TrackPD.model_validate(track.track) for track in result]

def get_preference_album_for_user(db: Session, id_user: int) -> List[AlbumPD]:
    with db() as session:
        query = select(UserAlbumPreference).where(UserAlbumPreference.user_id == id_user)
        result = session.execute(query).scalars().all()
        return [AlbumPD.model_validate(album.album) for album in result]


def get_track_preference_by_id(db: Session, preference_id: int) -> Optional[PreferenceTrackPD]:
    with db() as session:
        qeury = select(UserTrackPreference).where(UserTrackPreference.id == preference_id)
        result = session.execute(qeury).scalar_one_or_none()
        if not result:
            return None
        return PreferenceTrackPD.model_validate(result)

def get_album_preference_by_id(db: Session, preference_id: int) -> Optional[PreferenceAlbumPD]:
    with db() as session:
        qeury = select(UserAlbumPreference).where(UserAlbumPreference.id == preference_id)
        result = session.execute(qeury).scalar_one_or_none()
        if not result:
            return None
        return PreferenceAlbumPD.model_validate(result)


def add_track_preference(db: Session, user_id: int, track_id: int) -> PreferenceTrackPD:
    with db() as session:
        stmt = select(UserTrackPreference).where(
            UserTrackPreference.user_id == user_id,
            UserTrackPreference.track_id == track_id
        )
        existing = session.execute(stmt).scalar_one_or_none()

        if existing:
            return PreferenceTrackPD.from_orm(existing)

        new_preference = UserTrackPreference(user_id=user_id, track_id=track_id)
        session.add(new_preference)
        session.commit()
        session.refresh(new_preference)

        return PreferenceTrackPD.from_orm(new_preference)


def add_album_preference(db: Session, user_id: int, album_id: int) -> PreferenceAlbumPD:
    with db() as session:
        stmt = select(UserAlbumPreference).where(
            UserAlbumPreference.user_id == user_id,
            UserAlbumPreference.album_id == album_id
        )
        existing = session.execute(stmt).scalar_one_or_none()

        if existing:
            return PreferenceAlbumPD.from_orm(existing)

        new_preference = UserAlbumPreference(user_id=user_id, album_id=album_id)
        session.add(new_preference)
        session.commit()
        session.refresh(new_preference)

        return PreferenceAlbumPD.from_orm(new_preference)

def delete_preference_track_by_id(db: Session, id_track: int) -> Dict[str, str]:
    with db() as session:
        stmt = select(UserTrackPreference).where(UserTrackPreference.track_id == id_track)
        track = session.execute(stmt).scalar_one_or_none()
        if not track:
            return {"message": f"Не существует трека с id = {id_track}"}
        session.execute(delete(UserTrackPreference).where(UserTrackPreference.track_id == id_track))
        session.commit()
        return {"message": "ok"}

def delete_preference_album_by_id(db: Session, id_album: int) -> Dict[str, str]:
    with db() as session:
        stmt = select(UserAlbumPreference).where(UserAlbumPreference.album_id == id_album)
        track = session.execute(stmt).scalar_one_or_none()
        if not track:
            return {"message": f"Не существует альбома с id = {id_album}"}
        session.execute(delete(UserAlbumPreference).where(UserAlbumPreference.album_id == id_album))
        session.commit()
        return {"message": "ok"}