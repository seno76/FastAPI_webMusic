from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
class AuthorBase(BaseModel):
    id_user: int
    bio: str
    count_tracks: int = Field(ge=0)

class AuthorPD(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    id_user: int | None = None
    bio: str | None = None
    count_tracks: int | None = None

class AuthorPDData(AuthorPD):
    user: Optional['UserPD'] = None
    tracks: List['TrackPD'] = []
