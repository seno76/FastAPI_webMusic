from fastapi import APIRouter, HTTPException
from src.bd.database import session_factory
from typing import List, Dict
from datetime import date
from src.models.modelsPD import (
    TrackBase,
    TrackCreate,
    TrackPD,
    TrackPDData,
    TrackUpdate
)
from src.repository.trackRepository import (
    get_track_by_id,
    get_by_album,
    get_by_genre,
    get_top_rated,
    get_list_tracks,
    get_tracks_by_author,
    create_track,
    delete_track_by_id,
    update_data,
    get_released_after,
    search_by_title,
    get_average_rating,
    get_total_duration,
)
from src.core.security import security

router = APIRouter(
    prefix="/tracks",
    tags=["tracks"]
)

@router.get("/", response_model=List[TrackBase])
async def get_tracks() -> List[TrackPD]:
    return get_list_tracks(session_factory)

@router.get("/top", response_model=List[TrackPD])
async def get_top_tracks() -> List[TrackPD]:
    return get_top_rated(session_factory)

@router.get("/{id_track}", response_model=TrackPDData)
async def find_track_by_id(id_track: int) -> TrackPDData:
    track = get_track_by_id(session_factory, id_track)
    if not track:
        raise HTTPException(status_code=404, detail=f"Не найден трек с id = {id_track}")
    return track

@router.get("/by-album/{id_album}", response_model=List[TrackPD])
async def get_tracks_by_album(id_album: int) -> List[TrackPD]:
    return get_by_album(session_factory, id_album)


@router.get("/by-genre/{id_genre}", response_model=List[TrackPD])
async def get_tracks_by_genre(id_genre: int) -> List[TrackPD]:
    return get_by_genre(session_factory, id_genre)


@router.get("/by-author/{id_author}", response_model=List[TrackPD])
async def find_tracks_by_author(id_author: int) -> List[TrackPD]:
    return get_tracks_by_author(session_factory, id_author)

@router.post("/", response_model=TrackPD)
async def create_new_track(data: TrackCreate) -> TrackPD:
    return create_track(session_factory, data)

@router.put("/{id_track}", response_model=TrackPD)
async def update_track(id_track: int, data: TrackUpdate) -> TrackPD:
    return update_data(session_factory, id_track, data)

@router.get("/year/")
async def get_track_release_date(d: date) -> List[TrackPD]:
    return get_released_after(session_factory, d)

@router.get("/search/", response_model=List[TrackPD])
async def search(title: str) -> List[TrackPD]:
    return search_by_title(session_factory, title)

@router.get("/average/")
async def get_average():
    return get_average_rating(session_factory)

@router.get("/total/")
async def total():
    return get_total_duration(session_factory)

@router.delete("/", response_model=Dict[str, str])
async def delete(id_track: int) -> Dict[str, str]:
    res = delete_track_by_id(session_factory, id_track)
    if not res:
        raise HTTPException(status_code=404, detail=f"Не найден трек с id {id_track}")
    return {"status": "ok"}

