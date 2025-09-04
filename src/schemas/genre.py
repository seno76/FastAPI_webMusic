from pydantic import BaseModel, ConfigDict
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas import TrackPD, AlbumPD


class GenreBase(BaseModel):
    name: str
    description: str


class GenrePD(GenreBase):
    id: int
    is_delete: bool | None = False

    model_config = ConfigDict(from_attributes=True)


class GenreCreate(GenreBase):
    pass

class GenreUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_delete: bool | None = None

class GenrePDData(GenrePD):
    tracks: List['TrackPD'] = []
    albums: List['AlbumPD'] = []
