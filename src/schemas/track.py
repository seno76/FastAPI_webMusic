from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from pathlib import Path
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas import (
        AuthorPD,
        AlbumPD,
        GenrePD,
        PlayListPD,
        PreferenceTrackPDData,
    )


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
    pass

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
    author: Optional['AuthorPD'] = None
    album: Optional['AlbumPD'] = None
    genre: Optional['GenrePD'] = None
    playlist: List['PlayListPD'] = []
    user_preferences: List['PreferenceTrackPDData'] = []
