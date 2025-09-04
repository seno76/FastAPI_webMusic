from pydantic import BaseModel, HttpUrl, AnyUrl, Field, ConfigDict
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas import TrackPD, GenrePD, PreferenceAlbumPDData


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
    pass


class AlbumUpdate(BaseModel):
    genre_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=200)
    cover_url: Optional[AnyUrl] = None
    release_date: Optional[date] = None
    rating: Optional[float] = None


class AlbumPDData(AlbumPD):
    tracks: List["TrackPD"] = []
    genre: Optional["GenrePD"] = None
    user_preferences: List["PreferenceAlbumPDData"] = []
