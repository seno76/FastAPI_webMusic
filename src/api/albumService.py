from fastapi import APIRouter, Query, Path, HTTPException, Depends
from typing import List, Optional, Dict
from src.bd.database import session_factory
from src.models.modelsPD import AlbumPD, AlbumPDData, AlbumCreate, AlbumUpdate
from src.repository.albumRepository import (
    get_all_albums,
    get_album_by_id,
    create_album,
    update_album,
    get_albums_by_genre,
    delete_album_by_id,
)
from src.core.security import security

router = APIRouter(prefix="/albums", tags=["Albums"])

@router.get("/", response_model=List[AlbumPDData], dependencies=[Depends(security.access_token_required)])
async def list_albums(offset: int = Query(0, ge=0), limit: int = Query(100, le=500)):
    return get_all_albums(session_factory, offset=offset, limit=limit)

@router.get("/{album_id}", response_model=AlbumPDData)
async def get_album(album_id: int = Path(..., ge=1)):
    album = get_album_by_id(session_factory, album_id)
    if not album:
        raise HTTPException(status_code=404, detail=f"Альбом с id = {album_id} не найден!")
    return album

@router.post("/", response_model=AlbumPD)
async def add_album(album_data: AlbumCreate):
    return create_album(session_factory, album_data)

@router.put("/{album_id}", response_model=Optional[AlbumPD])
async def edit_album(album_id: int, album_data: AlbumUpdate):
    return update_album(session_factory, album_id, album_data)

@router.delete("/{album_id}")
async def remove_album(album_id: int) -> Dict[str, str]:
    if not delete_album_by_id(session_factory, album_id):
        raise HTTPException(status_code=404, detail=f"Album with id = {album_id} not found!")
    return {"message": f"Album with id = {album_id} was delited"}

@router.get("/search/by-genre/{genre_id}", response_model=List[AlbumPDData])
async def find_albums_by_genre(genre_id: int, offset: int = 0, limit: int = 1000):
    return get_albums_by_genre(session_factory, genre_id, limit=limit, offset=offset)
