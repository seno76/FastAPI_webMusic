from fastapi import APIRouter, HTTPException
from src.bd.database import session_factory
from typing import List, Dict
from src.models.modelsPD import (
    PlayListBase,
    PlayListCreate,
    PlayListUpdate,
    PlayListPD,
    PlayListPDData,
    TrackPD
)
from src.repository.playlistRepository import (
    add_track_to_playlist,
    delete_playlist,
    create_playlist,
    get_playlists,
    get_playlist_by_id,
    update_by_id,
    get_tracks_by_playlist,
)

router = APIRouter(
    prefix="/playlists",
    tags=["Playlists"]
)
from src.core.security import security

@router.get("/", response_model=List[PlayListPD])
async def playlists(limit: int = 1000, offset: int = 0) -> List[PlayListPD]:
    return get_playlists(session_factory, limit, offset)

@router.get("/{playlist_id}/tracks", response_model=List[TrackPD])
async def get_tracks(playlist_id: int) -> List[TrackPD]:
    tracks = get_tracks_by_playlist(session_factory, playlist_id)
    if not tracks:
        raise HTTPException(status_code=404, detail=f"Не найден плейлист с id = {playlist_id}")
    return tracks


@router.get("/{id_playlist}", response_model=PlayListPDData)
async def find_playlist_by_id(id_playlist: int) -> PlayListPDData:
    playlist = get_playlist_by_id(session_factory, id_playlist)
    if not playlist:
        raise HTTPException(status_code=404, detail=f"Не найден плейлист с id = {id_playlist}")
    return playlist

@router.patch("/{id_playlist}", response_model=PlayListPDData)
async def update_playlist(id_playlist: int, data: PlayListUpdate) -> PlayListPDData:
    return update_by_id(session_factory, id_playlist, data)

@router.post('/', response_model=PlayListBase)
async def create_new_playlist(data: PlayListCreate) -> PlayListPD:
    return create_playlist(session_factory, data)

@router.delete("/delete/{id_playlist}", response_model=Dict[str, str])
async def delete(id_playlist: int) -> Dict[str, str]:
    if not delete_playlist(session_factory, id_playlist):
        raise HTTPException(status_code=404, detail=f"Не найден плейлист с id = {id_playlist}")
    return {"status": "ok"}


@router.put("/add-track/{id_playlist}/{id_track}", response_model=PlayListPDData)
async def add_track(id_playlist: int, id_track: int, order: int) -> PlayListPDData:
    playlist = add_track_to_playlist(session_factory, id_playlist, id_track, order)
    if not playlist:
        raise HTTPException(status_code=404, detail="Не найден плейлист или трек")
    return playlist
