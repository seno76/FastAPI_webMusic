from typing import List, Optional, Dict
from src.models.modelsPD import PreferenceTrackPD, PreferenceAlbumPD, TrackPD, AlbumPD
from src.utils.abstractions import AbstractRepository


class UserTrackPreferenceService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository()
    
    def get_all_track_preferences(self, limit: int = 1000, offset: int = 0) -> List[PreferenceTrackPD]:
        return self.repository.get_all_track_preferences(limit, offset)
    
    def get_track_preference_by_id(self, preference_id: int) -> Optional[PreferenceTrackPD]:
        return self.repository.get_track_preference_by_id(preference_id)
    
    def get_track_preferences_for_user(self, user_id: int) -> List[TrackPD]:
        return self.repository.get_track_preferences_for_user(user_id)
    
    def add_track_preference(self, user_id: int, track_id: int) -> PreferenceTrackPD:
        return self.repository.add_track_preference(user_id, track_id)
    
    def delete_track_preference(self, preference_id: int) -> bool:
        return self.repository.delete_track_preference(preference_id)
    
    def delete_track_preference_by_track_id(self, track_id: int) -> bool:
        return self.repository.delete_track_preference_by_track_id(track_id)


class UserAlbumPreferenceService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository()
    
    def get_all_album_preferences(self, limit: int = 1000, offset: int = 0) -> List[PreferenceAlbumPD]:
        return self.repository.get_all_album_preferences(limit, offset)
    
    def get_album_preference_by_id(self, preference_id: int) -> Optional[PreferenceAlbumPD]:
        return self.repository.get_album_preference_by_id(preference_id)
    
    def get_album_preferences_for_user(self, user_id: int) -> List[AlbumPD]:
        return self.repository.get_album_preferences_for_user(user_id)
    
    def add_album_preference(self, user_id: int, album_id: int) -> PreferenceAlbumPD:
        return self.repository.add_album_preference(user_id, album_id)
    
    def delete_album_preference(self, preference_id: int) -> bool:
        return self.repository.delete_album_preference(preference_id)
    
    def delete_album_preference_by_album_id(self, album_id: int) -> bool:
        return self.repository.delete_album_preference_by_album_id(album_id)
    
