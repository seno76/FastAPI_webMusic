from src.schemas import (
    PlayListCreate,
    PlayListUpdate,
    PlayListPD,
    PlayListPDData,
    TrackPD,
)
from src.utils.abstractions import AbstractRepository
from typing import List, Optional


class PlayListService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository()
    
    def create_playlist(self, data: PlayListCreate) -> PlayListPD:
        return self.repository.create_playlist(data)
    
    def delete_playlist(self, playlist_id: int) -> bool:
        return self.repository.delete_playlist(playlist_id)
    
    def add_track_to_playlist(self, playlist_id: int, track_id: int, order: int) -> Optional[PlayListPDData]:
        return self.repository.add_track_to_playlist(playlist_id, track_id, order)
    
    def get_all_playlists(self, offset: int = 0, limit: int = 1000) -> List[PlayListPD]:
        return self.repository.get_all_playlists(offset, limit)
    
    def get_playlist_by_id(self, playlist_id: int) -> Optional[PlayListPDData]:
        return self.repository.get_playlist_by_id(playlist_id)
    
    def update_playlist(self, playlist_id: int, data: PlayListUpdate) -> Optional[PlayListPDData]:
        return self.repository.update_playlist(playlist_id, data)
    
    def get_tracks_by_playlist(self, playlist_id: int) -> Optional[List[TrackPD]]:
        return self.repository.get_tracks_by_playlist(playlist_id)
