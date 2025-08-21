from fastapi import APIRouter, HTTPException
from src.bd.database import session_factory
from src.models.modelsPD import (
    PreferenceTrackPD,
    PreferenceAlbumPD,
    TrackPD,
    AlbumPD
)
from typing import List, Dict
from src.repository.userPreferenceRepository import (
    get_all_tracks_preference,
    get_all_albums_preference,
    get_preference_album_for_user,
    get_preference_track_for_user,
    get_track_preference_by_id,
    get_album_preference_by_id,
    add_track_preference,
    add_album_preference,
    delete_preference_track_by_id,
    delete_preference_album_by_id
)

router = APIRouter(
    prefix="/preference",
    tags=["Preferences"],
)


@router.get("/tracks", response_model=List[PreferenceTrackPD])
async def get_tracks(limit: int = 1000, offset: int = 0) -> List[PreferenceTrackPD]:
    return get_all_tracks_preference(session_factory, limit, offset)

@router.get("/albums", response_model=List[PreferenceAlbumPD])
async def get_albums(limit: int = 1000, offset: int = 0) -> List[PreferenceAlbumPD]:
    return get_all_albums_preference(session_factory, limit, offset)


@router.get("/users/{id_user}/tracks", response_model=List[TrackPD])
async def get_all_tracks_for_user(id_user: int) -> List[TrackPD]:
    return get_preference_track_for_user(session_factory, id_user)

@router.get("/users/{id_user}/albums", response_model=List[AlbumPD])
async def get_all_albums_for_user(id_user: int) -> List[AlbumPD]:
    return get_preference_album_for_user(session_factory, id_user)

@router.get("/tracks/{id_preference}", response_model=PreferenceTrackPD)
async def get_preference_track(id_preference: int) -> PreferenceTrackPD:
    res = get_track_preference_by_id(session_factory, id_preference)
    if not res:
        raise HTTPException(status_code=404, detail=f"Не найдено предпочтение с id = {id_preference}")
    return res

@router.get("/albums/{id_preference}", response_model=PreferenceAlbumPD)
async def get_preference_album(id_preference: int) -> PreferenceAlbumPD:
    res = get_album_preference_by_id(session_factory, id_preference)
    if not res:
        raise HTTPException(status_code=404, detail=f"Не найдено предпочтение с id = {id_preference}")
    return res

@router.post("/users/{id_user}/tracks/{id_track}", response_model=PreferenceTrackPD)
async def add_preference_track(id_user: int, id_track: int) -> PreferenceTrackPD:
    return add_track_preference(session_factory, id_user, id_track)

@router.post("/users/{id_user}/albums/{id_album}", response_model=PreferenceAlbumPD)
async def add_preference_album(id_user: int, id_album: int) -> PreferenceAlbumPD:
    return add_album_preference(session_factory, id_user, id_album)


@router.delete("/tracks/{id_track}", response_model=Dict[str, str])
async def delete_track(id_track: int) -> Dict[str, str]:
    return delete_preference_track_by_id(session_factory, id_track)

@router.delete("/albums/{id_album}", response_model=Dict[str, str])
async def delete_album(id_album: int) -> Dict[str, str]:
    return delete_preference_album_by_id(session_factory, id_album)
