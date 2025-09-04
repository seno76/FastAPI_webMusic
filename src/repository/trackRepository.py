from sqlalchemy.orm import selectinload
from typing import Optional, List
from sqlalchemy import select, func
from src.models.modelsORM import Track
from src.schemas import TrackPD, TrackPDData, TrackCreate, TrackUpdate
from src.utils.abstractions import SQLAlchemyRepository
from src.bd.database import session_factory
from datetime import date


class TrackRepository(SQLAlchemyRepository):
    model = Track

    def get_track_by_id(self, track_id: int) -> Optional[TrackPDData]:
        with session_factory() as session:
            track = session.scalar(
                select(self.model)
                .options(
                    selectinload(self.model.author),
                    selectinload(self.model.album),
                    selectinload(self.model.genre),
                )
                .where(self.model.id == track_id)
            )
            if not track:
                return None
            return TrackPDData.model_validate(track)

    def create_track(self, data: TrackCreate) -> TrackPD:
        with session_factory() as session:
            track = self.model(**data.model_dump())
            track.file_path = str(track.file_path)
            session.add(track)
            session.commit()
            session.refresh(track)
            return TrackPD.model_validate(track)

    def delete_track(self, track_id: int) -> bool:
        with session_factory() as session:
            track = session.get(self.model, track_id)
            if not track:
                return False
            session.delete(track)
            session.commit()
            return True

    def get_all_tracks(self, limit: int = 100, offset: int = 0) -> List[TrackPD]:
        with session_factory() as session:
            query = select(self.model).offset(offset).limit(limit)
            tracks = session.execute(query).scalars().all()
            return [TrackPD.model_validate(track) for track in tracks]

    def update_track(self, track_id: int, data: TrackUpdate) -> Optional[TrackPD]:
        with session_factory() as session:
            track = session.get(self.model, track_id)
            if not track:
                return None

            update_data = data.model_dump(exclude_unset=True)
            if "file_path" in update_data:
                update_data["file_path"] = str(update_data["file_path"])

            for field, value in update_data.items():
                setattr(track, field, value)

            session.commit()
            session.refresh(track)
            return TrackPD.model_validate(track)

    def get_tracks_by_author(self, author_id: int) -> List[TrackPD]:
        with session_factory() as session:
            query = select(self.model).where(self.model.author_id == author_id)
            tracks = session.execute(query).scalars().all()
            return [TrackPD.model_validate(track) for track in tracks]

    def get_tracks_by_album(self, album_id: int) -> List[TrackPD]:
        with session_factory() as session:
            query = select(self.model).where(self.model.album_id == album_id)
            tracks = session.execute(query).scalars().all()
            return [TrackPD.model_validate(track) for track in tracks]

    def get_tracks_by_genre(self, genre_id: int) -> List[TrackPD]:
        with session_factory() as session:
            query = select(self.model).where(self.model.genre_id == genre_id)
            tracks = session.execute(query).scalars().all()
            return [TrackPD.model_validate(track) for track in tracks]

    def get_tracks_released_after(self, release_date: date) -> List[TrackPD]:
        with session_factory() as session:
            query = select(self.model).where(self.model.release_date >= release_date)
            tracks = session.execute(query).scalars().all()
            return [TrackPD.model_validate(track) for track in tracks]

    def get_top_rated_tracks(self, limit: int = 100) -> List[TrackPD]:
        with session_factory() as session:
            query = select(self.model).order_by(self.model.rating.desc()).limit(limit)
            tracks = session.execute(query).scalars().all()
            return [TrackPD.model_validate(track) for track in tracks]

    def search_tracks_by_title(self, title_query: str) -> List[TrackPD]:
        with session_factory() as session:
            query = select(self.model).where(
                func.lower(self.model.title).contains(func.lower(title_query))
            )
            tracks = session.execute(query).scalars().all()
            return [TrackPD.model_validate(track) for track in tracks]

    def get_average_rating(self) -> float:
        with session_factory() as session:
            result = session.scalar(select(func.avg(self.model.rating)))
            return float(result) if result else 0.0

    def get_total_duration(self) -> int:
        with session_factory() as session:
            result = session.scalar(select(func.sum(self.model.duration)))
            return int(result) if result else 0
