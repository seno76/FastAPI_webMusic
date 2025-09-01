from pydantic import BaseModel, EmailStr, AnyUrl, ConfigDict, Field, field_validator, HttpUrl
from datetime import date, datetime
from typing import Optional, List
from pathlib import Path


# -----------------------------
# USERS
# -----------------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    is_active: bool
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("username", mode="before")
    def check_invalid_chars(cls, s: str) -> str:
        SPECIAL_CHARS_SIMPLE = '!@#$%^&*()-=+[]{};:\'"\\|,.<>/?`~ '
        for char in SPECIAL_CHARS_SIMPLE:
            if char in s:
                raise ValueError("Username can only contain letters, numbers and underscores")
        return s


class UserPD(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    ...

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password_hash: str | None = None
    is_active: bool | None = None
    created_at: datetime | None = None


class UserPDData(UserPD):
    author: Optional['AuthorPD'] = None
    playlists: List['PlayListPDData'] = []
    track_preferences: List['PreferenceTrackPDData'] = []
    album_preferences: List['PreferenceAlbumPDData'] = []


class UserLogin(BaseModel):
    username: str
    password_hash: str

# -----------------------------
# AUTHORS
# -----------------------------


class AuthorBase(BaseModel):
    id_user: int
    bio: str
    count_tracks: int = Field(ge=0)

class AuthorPD(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class AuthorCreate(AuthorBase):
    ...

class AuthorUpdate(BaseModel):
    id_user: int | None = None
    bio: str | None = None
    count_tracks: int | None = None

class AuthorPDData(AuthorPD):
    user: Optional[UserPD] = None
    tracks: List['TrackPD'] = []


# -----------------------------
# TRACKS
# -----------------------------
class TrackBase(BaseModel):
    author_id: int
    album_id: Optional[int]
    genre_id: int
    title: str = Field(max_length=200)
    duration: int = Field(ge=0)
    file_path: Path
    is_explicit: bool
    release_date: date
    created_at: datetime
    rating: float


class TrackPD(TrackBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TrackCreate(TrackBase):
    ...

class TrackUpdate(BaseModel):
    author_id: Optional[int] = None
    album_id: Optional[int] = None
    genre_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=200)
    duration: Optional[int] = Field(default=None, ge=0)
    file_path: Optional[Path] = None
    is_explicit: Optional[bool] = None
    release_date: Optional[date] = None
    created_at: Optional[datetime] = None
    rating: Optional[float] = None


class TrackPDData(TrackPD):
    author: Optional[AuthorPD] = None
    album: Optional['AlbumPD'] = None
    genre: Optional['GenrePD'] = None
    playlist: List['PlayListPD'] = []
    user_preferences: List['PreferenceTrackPDData'] = []


# -----------------------------
# ALBUMS
# -----------------------------
class AlbumBase(BaseModel):
    genre_id: int
    title: str = Field(max_length=200)
    cover_url: HttpUrl
    release_date: date
    rating: float


class AlbumPD(AlbumBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AlbumCreate(AlbumBase):
    ...


class AlbumUpdate(BaseModel):
    genre_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=200)
    cover_url: Optional[AnyUrl] = None
    release_date: Optional[date] = None
    rating: Optional[float] = None


class AlbumPDData(AlbumPD):
    tracks: List[TrackPD] = []
    genre: Optional['GenrePD'] = None
    user_preferences: List['PreferenceAlbumPDData'] = []


# -----------------------------
# GENRES
# -----------------------------
class GenreBase(BaseModel):
    name: str
    description: str


class GenrePD(GenreBase):
    id: int
    is_delete: bool | None = False

    model_config = ConfigDict(from_attributes=True)


class GenreCreate(GenreBase):
    ...


class GenrePDData(GenrePD):
    tracks: List[TrackPD] = []
    albums: List[AlbumPD] = []


# -----------------------------
# PLAYLISTS
# -----------------------------
class PlayListBase(BaseModel):
    id_user: int
    title: str
    cover_url: AnyUrl
    all_time: int
    created_at: datetime


class PlayListPD(PlayListBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PlayListCreate(PlayListBase):
    ...


class PlayListUpdate(BaseModel):
    id_user: Optional[int] = None
    title: Optional[str] = None
    cover_url: Optional[AnyUrl] = None
    all_time: Optional[int] = None
    created_at: Optional[datetime] = None


class PlayListPDData(PlayListPD):
    tracks: List[TrackPD] = []


# -----------------------------
# PREFERENCES (разделённые)
# -----------------------------
class PreferenceAlbum(BaseModel):
    user_id: int
    album_id: int


class PreferenceAlbumPD(PreferenceAlbum):
    id: int
    album: Optional[AlbumPD] = None
    model_config = ConfigDict(from_attributes=True)


class PreferenceAlbumPDData(PreferenceAlbumPD):
    user: Optional[UserPD] = None


class PreferenceTrack(BaseModel):
    user_id: int
    track_id: int


class PreferenceTrackPD(PreferenceTrack):
    id: int
    track: Optional[TrackPD] = None
    model_config = ConfigDict(from_attributes=True)


class PreferenceTrackPDData(PreferenceTrackPD):
    user: Optional[UserPD] = None



# -----------------------------
# SIMPLE WRAPPER для объединённых предпочтений
# -----------------------------
class Preference(BaseModel):
    user_id: int
    albums: List[AlbumPD] = []
    tracks: List[TrackPD] = []
    model_config = ConfigDict(from_attributes=True)


__all__ = [
    # Users
    "UserBase",
    "UserPD",
    "UserCreate",
    "UserUpdate",
    "UserPDData",
    "UserLogin",

    # Authors
    "AuthorBase",
    "AuthorPD",
    "AuthorCreate",
    "AuthorUpdate",
    "AuthorPDData",

    # Tracks
    "TrackBase",
    "TrackPD",
    "TrackCreate",
    "TrackUpdate",
    "TrackPDData",

    # Albums
    "AlbumBase",
    "AlbumPD",
    "AlbumCreate",
    "AlbumUpdate",
    "AlbumPDData",

    # Genres
    "GenreBase",
    "GenrePD",
    "GenreCreate",
    "GenrePDData",

    # Playlists
    "PlayListBase",
    "PlayListPD",
    "PlayListCreate",
    "PlayListUpdate",
    "PlayListPDData",

    # Preferences
    "PreferenceAlbum",
    "PreferenceAlbumPD",
    "PreferenceAlbumPDData",
    "PreferenceTrack",
    "PreferenceTrackPD",
    "PreferenceTrackPDData",

    # Wrapper
    "Preference",
]