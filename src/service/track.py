from src.models.modelsPD import TrackCreate, TrackUpdate, TrackPD, TrackPDData
from src.utils.abstractions import AbstractRepository
from typing import List, Optional
from datetime import date


class TrackService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository()
    
    def get_track_by_id(self, track_id: int) -> Optional[TrackPDData]:
        return self.repository.get_track_by_id(track_id)
    
    def create_track(self, data: TrackCreate) -> TrackPD:
        return self.repository.create_track(data)
    
    def delete_track(self, track_id: int) -> bool:
        return self.repository.delete_track(track_id)
    
    def get_all_tracks(self, limit: int = 100, offset: int = 0) -> List[TrackPD]:
        return self.repository.get_all_tracks(limit, offset)
    
    def update_track(self, track_id: int, data: TrackUpdate) -> Optional[TrackPD]:
        return self.repository.update_track(track_id, data)
    
    def get_tracks_by_author(self, author_id: int) -> List[TrackPD]:
        return self.repository.get_tracks_by_author(author_id)
    
    def get_tracks_by_album(self, album_id: int) -> List[TrackPD]:
        return self.repository.get_tracks_by_album(album_id)
    
    def get_tracks_by_genre(self, genre_id: int) -> List[TrackPD]:
        return self.repository.get_tracks_by_genre(genre_id)
    
    def get_tracks_released_after(self, release_date: date) -> List[TrackPD]:
        return self.repository.get_tracks_released_after(release_date)
    
    def get_top_rated_tracks(self, limit: int = 100) -> List[TrackPD]:
        return self.repository.get_top_rated_tracks(limit)
    
    def search_tracks_by_title(self, title_query: str) -> List[TrackPD]:
        return self.repository.search_tracks_by_title(title_query)
    
    def get_average_rating(self) -> float:
        return self.repository.get_average_rating()
    
    def get_total_duration(self) -> int:
        return self.repository.get_total_duration()