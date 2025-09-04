from pydantic import BaseModel, AnyUrl, ConfigDict
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas import TrackPD


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
    pass


class PlayListUpdate(BaseModel):
    id_user: Optional[int] = None
    title: Optional[str] = None
    cover_url: Optional[AnyUrl] = None
    all_time: Optional[int] = None
    created_at: Optional[datetime] = None


class PlayListPDData(PlayListPD):
    tracks: List['TrackPD'] = []
