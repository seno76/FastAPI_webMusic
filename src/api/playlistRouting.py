from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from src.models.modelsPD import (
    PlayListBase,
    PlayListCreate,
    PlayListUpdate,
    PlayListPD,
    PlayListPDData,
    TrackPD
)
from src.core.security import security
from src.service.playlist import PlayListService
from src.core.depends import playlist_service_dep

router = APIRouter(prefix="/playlists", tags=["Playlists"])


@router.get("/", response_model=List[PlayListPD])
async def playlists(
    limit: int = 1000,
    offset: int = 0,
    playlist_service: PlayListService = Depends(playlist_service_dep),
) -> List[PlayListPD]:
    return playlist_service.get_all_playlists(offset, limit)


@router.get("/{playlist_id}/tracks", response_model=List[TrackPD])
async def get_tracks(
    playlist_id: int, playlist_service: PlayListService = Depends(playlist_service_dep)
) -> List[TrackPD]:
    tracks = playlist_service.get_tracks_by_playlist(playlist_id)
    if not tracks:
        raise HTTPException(status_code=404, detail=f"Не найден плейлист с id = {playlist_id}")
    return tracks


@router.get("/{playlist_id}", response_model=PlayListPDData)
async def find_playlist_by_id(
    playlist_id: int, playlist_service: PlayListService = Depends(playlist_service_dep)
) -> PlayListPDData:
    playlist = playlist_service.get_playlist_by_id(playlist_id)
    if not playlist:
        raise HTTPException(
            status_code=404, detail=f"Не найден плейлист с id = {playlist_id}"
        )
    return playlist


@router.patch(
    "/{playlist_id}",
    response_model=PlayListPDData,
    dependencies=[Depends(security.access_token_required)],
)
async def update_playlist(
    playlist_id: int,
    data: PlayListUpdate,
    playlist_service: PlayListService = Depends(playlist_service_dep),
) -> PlayListPDData:
    updated_playlist = playlist_service.update_playlist(playlist_id, data)
    if not updated_playlist:
        raise HTTPException(
            status_code=404, detail=f"Не найден плейлист с id = {playlist_id}"
        )
    return updated_playlist


@router.post(
    "/",
    response_model=PlayListPD,
    dependencies=[Depends(security.access_token_required)],
)
async def create_new_playlist(
    data: PlayListCreate,
    playlist_service: PlayListService = Depends(playlist_service_dep),
) -> PlayListPD:
    return playlist_service.create_playlist(data)


@router.delete(
    "/{playlist_id}",
    response_model=Dict[str, str],
    dependencies=[Depends(security.access_token_required)],
)
async def delete_playlist(
    playlist_id: int, playlist_service: PlayListService = Depends(playlist_service_dep)
) -> Dict[str, str]:
    if not playlist_service.delete_playlist(playlist_id):
        raise HTTPException(
            status_code=404, detail=f"Не найден плейлист с id = {playlist_id}"
        )
    return {"status": "ok"}


@router.put(
    "/{playlist_id}/tracks/{track_id}",
    response_model=PlayListPDData,
    dependencies=[Depends(security.access_token_required)],
)
async def add_track_to_playlist(
    playlist_id: int,
    track_id: int,
    order: int,
    playlist_service: PlayListService = Depends(playlist_service_dep),
) -> PlayListPDData:
    playlist = playlist_service.add_track_to_playlist(playlist_id, track_id, order)
    if not playlist:
        raise HTTPException(status_code=404, detail="Не найден плейлист или трек")
    return playlist
