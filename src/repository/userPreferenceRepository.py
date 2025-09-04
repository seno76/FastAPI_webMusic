from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional
from src.models.modelsORM import UserTrackPreference, UserAlbumPreference
from src.schemas import PreferenceTrackPD, PreferenceAlbumPD, TrackPD, AlbumPD
from src.utils.abstractions import SQLAlchemyRepository
from src.bd.database import session_factory


class UserTrackPreferenceRepository(SQLAlchemyRepository):
    model = UserTrackPreference

    def get_all_track_preferences(
        self, limit: int = 1000, offset: int = 0
    ) -> List[PreferenceTrackPD]:
        with session_factory() as session:
            query = select(self.model).limit(limit).offset(offset)
            preferences = session.execute(query).scalars().all()
            return [PreferenceTrackPD.model_validate(pref) for pref in preferences]

    def get_track_preference_by_id(
        self, preference_id: int
    ) -> Optional[PreferenceTrackPD]:
        with session_factory() as session:
            preference = session.get(self.model, preference_id)
            if not preference:
                return None
            return PreferenceTrackPD.model_validate(preference)

    def get_track_preferences_for_user(self, user_id: int) -> List[TrackPD]:
        with session_factory() as session:
            query = (
                select(self.model)
                .where(self.model.user_id == user_id)
                .options(selectinload(self.model.track))
            )
            preferences = session.execute(query).scalars().all()
            return [TrackPD.model_validate(pref.track) for pref in preferences]

    def add_track_preference(self, user_id: int, track_id: int) -> PreferenceTrackPD:
        with session_factory() as session:
            # Проверяем существование предпочтения
            existing = session.scalar(
                select(self.model).where(
                    self.model.user_id == user_id, self.model.track_id == track_id
                )
            )

            if existing:
                return PreferenceTrackPD.model_validate(existing)

            # Создаем новое предпочтение
            new_preference = self.model(user_id=user_id, track_id=track_id)
            session.add(new_preference)
            session.commit()
            session.refresh(new_preference)
            return PreferenceTrackPD.model_validate(new_preference)

    def delete_track_preference(self, preference_id: int) -> bool:
        with session_factory() as session:
            preference = session.get(self.model, preference_id)
            if not preference:
                return False
            session.delete(preference)
            session.commit()
            return True

    def delete_track_preference_by_track_id(self, track_id: int) -> bool:
        with session_factory() as session:
            result = session.execute(
                delete(self.model).where(self.model.track_id == track_id)
            )
            session.commit()
            return result.rowcount > 0


class UserAlbumPreferenceRepository(SQLAlchemyRepository):
    model = UserAlbumPreference

    def get_all_album_preferences(
        self, limit: int = 1000, offset: int = 0
    ) -> List[PreferenceAlbumPD]:
        with session_factory() as session:
            query = select(self.model).limit(limit).offset(offset)
            preferences = session.execute(query).scalars().all()
            return [PreferenceAlbumPD.model_validate(pref) for pref in preferences]

    def get_album_preference_by_id(
        self, preference_id: int
    ) -> Optional[PreferenceAlbumPD]:
        with session_factory() as session:
            preference = session.get(self.model, preference_id)
            if not preference:
                return None
            return PreferenceAlbumPD.model_validate(preference)

    def get_album_preferences_for_user(self, user_id: int) -> List[AlbumPD]:
        with session_factory() as session:
            query = (
                select(self.model)
                .where(self.model.user_id == user_id)
                .options(selectinload(self.model.album))
            )
            preferences = session.execute(query).scalars().all()
            return [AlbumPD.model_validate(pref.album) for pref in preferences]

    def add_album_preference(self, user_id: int, album_id: int) -> PreferenceAlbumPD:
        with session_factory() as session:
            # Проверяем существование предпочтения
            existing = session.scalar(
                select(self.model).where(
                    self.model.user_id == user_id, self.model.album_id == album_id
                )
            )

            if existing:
                return PreferenceAlbumPD.model_validate(existing)

            # Создаем новое предпочтение
            new_preference = self.model(user_id=user_id, album_id=album_id)
            session.add(new_preference)
            session.commit()
            session.refresh(new_preference)
            return PreferenceAlbumPD.model_validate(new_preference)

    def delete_album_preference(self, preference_id: int) -> bool:
        with session_factory() as session:
            preference = session.get(self.model, preference_id)
            if not preference:
                return False
            session.delete(preference)
            session.commit()
            return True

    def delete_album_preference_by_album_id(self, album_id: int) -> bool:
        with session_factory() as session:
            result = session.execute(
                delete(self.model).where(self.model.album_id == album_id)
            )
            session.commit()
            return result.rowcount > 0
