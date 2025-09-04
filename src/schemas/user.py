from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas import (
        AuthorPD,
        PlayListPDData,
        PreferenceTrackPDData,
        PreferenceAlbumPDData,
    )


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
    pass

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
