from pydantic import BaseModel, ConfigDict
from typing import Optional, List




class PreferenceAlbum(BaseModel):
    user_id: int
    album_id: int


class PreferenceAlbumPD(PreferenceAlbum):
    id: int
    album: Optional['AlbumPD'] = None
    model_config = ConfigDict(from_attributes=True)


class PreferenceAlbumPDData(PreferenceAlbumPD):
    user: Optional['UserPD'] = None


class PreferenceTrack(BaseModel):
    user_id: int
    track_id: int


class PreferenceTrackPD(PreferenceTrack):
    id: int
    track: Optional['TrackPD'] = None
    model_config = ConfigDict(from_attributes=True)


class PreferenceTrackPDData(PreferenceTrackPD):
    user: Optional['UserPD'] = None


class Preference(BaseModel):
    user_id: int
    albums: List['AlbumPD'] = []
    tracks: List['TrackPD'] = []
    model_config = ConfigDict(from_attributes=True)

