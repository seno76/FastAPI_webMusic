from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from sqlalchemy import select, insert
from src.models.modelsORM import PlayList, PlaylistTrack, Track
from src.models.modelsPD import (
    PlayListUpdate,
    PlayListCreate,
    PlayListPD,
    PlayListPDData,
    TrackPD,
)
from src.utils.abstractions import SQLAlchemyRepository
from src.bd.database import session_factory


class PlayListRepository(SQLAlchemyRepository):
    model = PlayList

    def create_playlist(self, data: PlayListCreate) -> PlayListPD:
        with session_factory() as session:
            playlist = self.model(**data.model_dump())
            playlist.cover_url = str(playlist.cover_url)
            session.add(playlist)
            session.commit()
            session.refresh(playlist)
            return PlayListPD.model_validate(playlist)

    def delete_playlist(self, playlist_id: int) -> bool:
        with session_factory() as session:
            playlist = session.scalar(
                select(self.model).where(self.model.id == playlist_id)
            )
            if not playlist:
                return False

            session.delete(playlist)
            session.commit()
            return True

    def add_track_to_playlist(
        self, playlist_id: int, track_id: int, order: int
    ) -> Optional[PlayListPDData]:
        with session_factory() as session:
            # Проверяем существование плейлиста и трека
            playlist_exists = session.scalar(
                select(self.model.id).where(self.model.id == playlist_id)
            )
            track_exists = session.scalar(select(Track.id).where(Track.id == track_id))

            if not playlist_exists or not track_exists:
                return None

            # Добавляем связь
            session.execute(
                insert(PlaylistTrack).values(
                    playlist_id=playlist_id, track_id=track_id, order=order
                )
            )
            session.commit()

            # Получаем обновленный плейлист с треками
            playlist = session.scalar(
                select(self.model)
                .where(self.model.id == playlist_id)
                .options(selectinload(self.model.tracks))
            )
            return PlayListPDData.model_validate(playlist)

    def get_all_playlists(self, offset: int = 0, limit: int = 1000) -> List[PlayListPD]:
        with session_factory() as session:
            query = select(self.model).limit(limit).offset(offset)
            playlists = session.execute(query).scalars().all()
            return [PlayListPD.model_validate(playlist) for playlist in playlists]

    def get_playlist_by_id(self, playlist_id: int) -> Optional[PlayListPDData]:
        with session_factory() as session:
            playlist = session.scalar(
                select(self.model)
                .where(self.model.id == playlist_id)
                .options(selectinload(self.model.tracks))
            )
            if not playlist:
                return None
            return PlayListPDData.model_validate(playlist)

    def update_playlist(
        self, playlist_id: int, data: PlayListUpdate
    ) -> Optional[PlayListPDData]:
        with session_factory() as session:
            playlist = session.scalar(
                select(self.model).where(self.model.id == playlist_id)
            )
            if not playlist:
                return None

            update_data = data.model_dump(exclude_unset=True)
            if "cover_url" in update_data:
                update_data["cover_url"] = str(update_data["cover_url"])

            for field, value in update_data.items():
                setattr(playlist, field, value)

            session.commit()
            session.refresh(playlist)

            # Загружаем связанные треки
            session.refresh(playlist, attribute_names=["tracks"])
            return PlayListPDData.model_validate(playlist)

    def get_tracks_by_playlist(self, playlist_id: int) -> Optional[List[TrackPD]]:
        with session_factory() as session:
            playlist = session.scalar(
                select(self.model)
                .where(self.model.id == playlist_id)
                .options(selectinload(self.model.tracks))
            )
            if not playlist:
                return None
            return [TrackPD.model_validate(track) for track in playlist.tracks]
