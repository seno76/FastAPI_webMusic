from src.models.modelsORM import UserTrackPreference
from src.repository import userPreferenceRepository
from src.repository.albumRepository import AlbumRepository
from src.repository.genreRepository import GenreRepository
from src.repository.playlistRepository import PlayListRepository
from src.repository.trackRepository import TrackRepository
from src.repository.userRepository import UserRepository
from src.repository.authorRepository import AuthorRepository
from src.repository.userPreferenceRepository import UserAlbumPreferenceRepository, UserTrackPreferenceRepository
from src.service.album import AlbumService
from src.service.genre import GenreService
from src.service.playlist import PlayListService
from src.service.track import TrackService
from src.service.user import UserService
from src.service.author import AuthorService
from src.service.userPreference import UserTrackPreferenceService, UserAlbumPreferenceService
from typing import Type, TypeVar, Generic
from src.utils.abstractions import AbstractRepository

T = TypeVar('T')

class ServiceDependency(Generic[T]):
    def __init__(self, service_class: Type[T], repository_class: Type[AbstractRepository]):
        self.service_class = service_class
        self.repository_class = repository_class
    
    def __call__(self) -> T:
        return self.service_class(self.repository_class)

# Создание зависимостей
user_service_dep = ServiceDependency(UserService, UserRepository)
author_service_dep = ServiceDependency(AuthorService, AuthorRepository)
album_service_dep = ServiceDependency(AlbumService, AlbumRepository)
genre_service_dep = ServiceDependency(GenreService, GenreRepository)
playlist_service_dep = ServiceDependency(PlayListService, PlayListRepository)
track_service_dep = ServiceDependency(TrackService, TrackRepository)
track_preference_service_dep = ServiceDependency(UserTrackPreferenceService, UserTrackPreferenceRepository)
album_preference_service_dep = ServiceDependency(UserAlbumPreferenceService, UserAlbumPreferenceRepository)