from .user import UserPD, UserPDData, UserCreate, UserUpdate, UserLogin
from .author import AuthorPD, AuthorPDData, AuthorCreate, AuthorUpdate
from .track import TrackPD, TrackPDData, TrackCreate, TrackUpdate, TrackBase
from .album import AlbumPD, AlbumPDData, AlbumCreate, AlbumUpdate
from .genre import GenrePD, GenrePDData, GenreCreate, GenreBase, GenreUpdate
from .playlist import PlayListPD, PlayListPDData, PlayListCreate, PlayListUpdate, PlayListBase
from .preference import (
    PreferenceAlbumPD, PreferenceAlbumPDData, 
    PreferenceTrackPD, PreferenceTrackPDData,
    PreferenceAlbum, PreferenceTrack, Preference
)

# Now rebuild all models with circular dependencies
# Rebuild in dependency order
GenrePDData.model_rebuild()
AlbumPDData.model_rebuild() 
TrackPDData.model_rebuild()
AuthorPDData.model_rebuild()
PlayListPDData.model_rebuild()
PreferenceAlbumPD.model_rebuild()
PreferenceAlbumPDData.model_rebuild()
PreferenceTrackPD.model_rebuild()
PreferenceTrackPDData.model_rebuild()
Preference.model_rebuild()
UserPDData.model_rebuild()


__all__ = [
    'UserPD', 'UserPDData', 'UserCreate', 'UserUpdate', 'UserLogin',
    'AuthorPD', 'AuthorPDData', 'AuthorCreate', 'AuthorUpdate',
    'TrackPD', 'TrackPDData', 'TrackCreate', 'TrackUpdate', 'TrackBase',
    'AlbumPD', 'AlbumPDData', 'AlbumCreate', 'AlbumUpdate',
    'GenrePD', 'GenrePDData', 'GenreCreate', 'GenreUpdate', 'GenreBases',
    'PlayListPD', 'PlayListPDData', 'PlayListCreate', 'PlayListUpdate', 'PlayListBase',
    'PreferenceAlbum', 'PreferenceAlbumPD', 'PreferenceAlbumPDData',
    'PreferenceTrack', 'PreferenceTrackPD', 'PreferenceTrackPDData',
    'Preference'
]