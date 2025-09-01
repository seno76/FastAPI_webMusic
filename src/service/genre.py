from src.models.modelsPD import GenreCreate
from src.utils.abstractions import AbstractRepository


class GenreService:
    
    def __init__(self, repository: AbstractRepository):
        self.repository = repository()
        
    def get_genres(self, offset=0, limit=100):
        return self.repository.get_all_genres(offset, limit)
    
    def get_genre(self, genre_id: int):
        return self.repository.get_genre_by_id(genre_id)
    
    def create_genre(self, data: GenreCreate):
        return self.repository.create_new_genre(data)
    
    def delete(self, genre_id):
        return self.repository.delete_genre(genre_id)