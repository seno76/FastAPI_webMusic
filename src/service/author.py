from typing import List, Optional
from src.schemas import AuthorCreate, AuthorUpdate, AuthorPDData
from src.utils.abstractions import AbstractRepository

class AuthorService:
    
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository: AbstractRepository = repository()
    
    def get_authors(self, offset: int = 0, limit: int = 100) -> List[AuthorPDData]:
        return self.repository.find_all(offset, limit)
    
    def get_author(self, author_id: int) -> Optional[AuthorPDData]:
        return self.repository.get_by_id(author_id)
    
    def get_author_by_user_id(self, user_id: int) -> Optional[AuthorPDData]:
        return self.repository.get_by_user_id(user_id)
    
    def create_author(self, data: AuthorCreate) -> AuthorPDData:
        return self.repository.create(data)
    
    def update_author(self, author_id: int, data: AuthorUpdate) -> Optional[AuthorPDData]:
        return self.repository.update(author_id, data)
    
    def delete_author(self, author_id: int) -> None:
        return self.repository.delete_by_id(author_id)
