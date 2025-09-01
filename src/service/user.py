from src.models.modelsPD import UserCreate
from src.utils.abstractions import AbstractRepository

class UserService:
    
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository: AbstractRepository = repository()
    
    def get_users(self):
        return self.repository.find_all()
    
    def create_user(self, user: UserCreate):
        users_dict = user.model_dump()
        return self.repository.create_user(users_dict)
    
    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id) 
    
    def get_active_users(self):
        return self.repository.is_active()
    
    def get_passive_users(self):
        return self.repository.is_passive()
    
    def get_user_by_name(self, username: str):
        return self.repository.by_username(username)
    
    def get_user_by_email(self, mail: str):
        return self.repository.user_by_email(mail)
    
    def set_status(self, user_id: int, status: bool):
        return self.repository.set_user_status(user_id, status)
    
    def count_users(self, only_active):
        return self.repository.count_users(only_active)
    
    def delete(self, id_user):
        return self.repository.delete_user_by_id(id_user)
    
    def get_playlist(self, id_user):
        return self.repository.get_plalylist_by_user_id(id_user)
    
    def login_user(self, username: str, password: str):
        return self.repository.auth_user(username, password)