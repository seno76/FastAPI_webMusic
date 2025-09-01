from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict
from src.models.modelsPD import PreferenceTrackPD, PreferenceAlbumPD, TrackPD, AlbumPD
from src.core.security import security
from src.service.userPreference import (
    UserTrackPreferenceService,
    UserAlbumPreferenceService,
)
from src.core.depends import track_preference_service_dep, album_preference_service_dep

router = APIRouter(
    prefix="/preferences",
    tags=["User Preferences"],
)


# Track Preferences
@router.get(
    "/tracks",
    response_model=List[PreferenceTrackPD],
    dependencies=[Depends(security.access_token_required)],
)
async def get_track_preferences(
    limit: int = Query(1000, le=1000),
    offset: int = Query(0, ge=0),
    track_service: UserTrackPreferenceService = Depends(track_preference_service_dep),
) -> List[PreferenceTrackPD]:
    return track_service.get_all_track_preferences(limit, offset)


@router.get(
    "/users/{user_id}/tracks",
    response_model=List[TrackPD],
    dependencies=[Depends(security.access_token_required)],
)
async def get_user_track_preferences(
    user_id: int,
    track_service: UserTrackPreferenceService = Depends(track_preference_service_dep),
) -> List[TrackPD]:
    return track_service.get_track_preferences_for_user(user_id)


@router.get(
    "/tracks/{preference_id}",
    response_model=PreferenceTrackPD,
    dependencies=[Depends(security.access_token_required)],
)
async def get_track_preference(
    preference_id: int,
    track_service: UserTrackPreferenceService = Depends(track_preference_service_dep),
) -> PreferenceTrackPD:
    preference = track_service.get_track_preference_by_id(preference_id)
    if not preference:
        raise HTTPException(
            status_code=404,
            detail=f"Предпочтение трека с id={preference_id} не найдено",
        )
    return preference


@router.post(
    "/users/{user_id}/tracks/{track_id}",
    response_model=PreferenceTrackPD,
    dependencies=[Depends(security.access_token_required)],
)
async def add_track_preference(
    user_id: int,
    track_id: int,
    track_service: UserTrackPreferenceService = Depends(track_preference_service_dep),
) -> PreferenceTrackPD:
    return track_service.add_track_preference(user_id, track_id)


@router.delete(
    "/tracks/{preference_id}",
    response_model=Dict[str, str],
    dependencies=[Depends(security.access_token_required)],
)
async def delete_track_preference(
    preference_id: int,
    track_service: UserTrackPreferenceService = Depends(track_preference_service_dep),
) -> Dict[str, str]:
    if not track_service.delete_track_preference(preference_id):
        raise HTTPException(
            status_code=404,
            detail=f"Предпочтение трека с id={preference_id} не найдено",
        )
    return {"message": "Предпочтение трека удалено"}


# Album Preferences
@router.get(
    "/albums",
    response_model=List[PreferenceAlbumPD],
    dependencies=[Depends(security.access_token_required)],
)
async def get_album_preferences(
    limit: int = Query(1000, le=1000),
    offset: int = Query(0, ge=0),
    album_service: UserAlbumPreferenceService = Depends(album_preference_service_dep),
) -> List[PreferenceAlbumPD]:
    return album_service.get_all_album_preferences(limit, offset)


@router.get(
    "/users/{user_id}/albums",
    response_model=List[AlbumPD],
    dependencies=[Depends(security.access_token_required)],
)
async def get_user_album_preferences(
    user_id: int,
    album_service: UserAlbumPreferenceService = Depends(album_preference_service_dep),
) -> List[AlbumPD]:
    return album_service.get_album_preferences_for_user(user_id)


@router.get(
    "/albums/{preference_id}",
    response_model=PreferenceAlbumPD,
    dependencies=[Depends(security.access_token_required)],
)
async def get_album_preference(
    preference_id: int,
    album_service: UserAlbumPreferenceService = Depends(album_preference_service_dep),
) -> PreferenceAlbumPD:
    preference = album_service.get_album_preference_by_id(preference_id)
    if not preference:
        raise HTTPException(
            status_code=404,
            detail=f"Предпочтение альбома с id={preference_id} не найдено",
        )
    return preference


@router.post(
    "/users/{user_id}/albums/{album_id}",
    response_model=PreferenceAlbumPD,
    dependencies=[Depends(security.access_token_required)],
)
async def add_album_preference(
    user_id: int,
    album_id: int,
    album_service: UserAlbumPreferenceService = Depends(album_preference_service_dep),
) -> PreferenceAlbumPD:
    return album_service.add_album_preference(user_id, album_id)


@router.delete(
    "/albums/{preference_id}",
    response_model=Dict[str, str],
    dependencies=[Depends(security.access_token_required)],
)
async def delete_album_preference(
    preference_id: int,
    album_service: UserAlbumPreferenceService = Depends(album_preference_service_dep),
) -> Dict[str, str]:
    if not album_service.delete_album_preference(preference_id):
        raise HTTPException(
            status_code=404,
            detail=f"Предпочтение альбома с id={preference_id} не найдено",
        )
    return {"message": "Предпочтение альбома удалено"}
