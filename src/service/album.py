import select

from urllib3 import Retry
from src.schemas.album import AlbumCreate, AlbumPD, AlbumUpdate
from src.utils.abstractions import AbstractRepository


class AlbumService:
    
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository: AbstractRepository = repository()
        
    def get_albums(self, limit: int = 100, offset: int = 0):
        return self.repository.get_all_albums(limit, offset)
    
    def get_album(self, id_album: int):
        return self.repository.get_album_by_id(id_album)
    
    def create_album(self, new_album: AlbumCreate):
        return self.repository.create_album(new_album)
    
    def delete_album(self, id_album: int):
        return self.repository.delete_album_by_id(id_album)
    
    def update_album(self, id_album: int, album_data: AlbumUpdate):
        return self.repository.update_album(id_album, album_data)
    
    def get_albums_genre(self, id_genre: int, limit: int = 100, offset: int = 0):
        return self.repository.get_albums_by_genre(id_genre, limit=limit, offset=offset)
