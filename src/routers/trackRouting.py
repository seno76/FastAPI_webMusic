from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict
from datetime import date
from src.schemas import (
    TrackBase,
    TrackCreate,
    TrackPD,
    TrackPDData,
    TrackUpdate,
)
from src.core.security import security
from src.service.track import TrackService
from src.core.depends import track_service_dep

router = APIRouter(prefix="/tracks", tags=["Tracks"])


@router.get("/", response_model=List[TrackBase])
async def get_tracks(
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0),
    track_service: TrackService = Depends(track_service_dep),
) -> List[TrackPD]:
    return track_service.get_all_tracks(limit, offset)


@router.get("/top-rated", response_model=List[TrackPD])
async def get_top_tracks(
    limit: int = Query(100, le=1000),
    track_service: TrackService = Depends(track_service_dep),
) -> List[TrackPD]:
    return track_service.get_top_rated_tracks(limit)


@router.get("/{track_id}", response_model=TrackPDData)
async def get_track_by_id(
    track_id: int, track_service: TrackService = Depends(track_service_dep)
) -> TrackPDData:
    track = track_service.get_track_by_id(track_id)
    if not track:
        raise HTTPException(status_code=404, detail=f"Трек с id={track_id} не найден")
    return track


@router.get("/album/{album_id}", response_model=List[TrackPD])
async def get_tracks_by_album(
    album_id: int, track_service: TrackService = Depends(track_service_dep)
) -> List[TrackPD]:
    return track_service.get_tracks_by_album(album_id)


@router.get("/genre/{genre_id}", response_model=List[TrackPD])
async def get_tracks_by_genre(
    genre_id: int, track_service: TrackService = Depends(track_service_dep)
) -> List[TrackPD]:
    return track_service.get_tracks_by_genre(genre_id)


@router.get("/author/{author_id}", response_model=List[TrackPD])
async def get_tracks_by_author(
    author_id: int, track_service: TrackService = Depends(track_service_dep)
) -> List[TrackPD]:
    return track_service.get_tracks_by_author(author_id)


@router.post(
    "/", response_model=TrackPD, dependencies=[Depends(security.access_token_required)]
)
async def create_track(
    data: TrackCreate, track_service: TrackService = Depends(track_service_dep)
) -> TrackPD:
    return track_service.create_track(data)


@router.put(
    "/{track_id}",
    response_model=TrackPD,
    dependencies=[Depends(security.access_token_required)],
)
async def update_track(
    track_id: int,
    data: TrackUpdate,
    track_service: TrackService = Depends(track_service_dep),
) -> TrackPD:
    updated_track = track_service.update_track(track_id, data)
    if not updated_track:
        raise HTTPException(status_code=404, detail=f"Трек с id={track_id} не найден")
    return updated_track


@router.get("/released-after/", response_model=List[TrackPD])
async def get_tracks_released_after(
    release_date: date, track_service: TrackService = Depends(track_service_dep)
) -> List[TrackPD]:
    return track_service.get_tracks_released_after(release_date)


@router.get("/search/", response_model=List[TrackPD])
async def search_tracks(
    title: str, track_service: TrackService = Depends(track_service_dep)
) -> List[TrackPD]:
    return track_service.search_tracks_by_title(title)


@router.get("/stats/average-rating")
async def get_average_rating(
    track_service: TrackService = Depends(track_service_dep),
) -> Dict[str, float]:
    return {"average_rating": track_service.get_average_rating()}


@router.get("/stats/total-duration")
async def get_total_duration(
    track_service: TrackService = Depends(track_service_dep),
) -> Dict[str, int]:
    return {"total_duration_seconds": track_service.get_total_duration()}


@router.delete(
    "/{track_id}",
    response_model=Dict[str, str],
    dependencies=[Depends(security.access_token_required)],
)
async def delete_track(
    track_id: int, track_service: TrackService = Depends(track_service_dep)
) -> Dict[str, str]:
    if not track_service.delete_track(track_id):
        raise HTTPException(status_code=404, detail=f"Трек с id={track_id} не найден")
    return {"status": "ok", "message": f"Трек с id={track_id} удален"}
