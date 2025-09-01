from fastapi import APIRouter, Query, Path, HTTPException, Depends
from typing import List, Optional, Dict
from src.bd.database import session_factory
from src.models.modelsPD import AlbumPD, AlbumPDData, AlbumCreate, AlbumUpdate
from src.core.depends import album_service_dep
from src.core.security import security
from src.service import album
from src.service.album import AlbumService

router = APIRouter(prefix="/albums", tags=["Albums"])

@router.get("/", response_model=List[AlbumPDData])
async def list_albums(
    offset: int = Query(0, ge=0), limit: int = Query(100, le=500),
    album_service: AlbumService = Depends(album_service_dep)
):
    return album_service.get_albums(offset=offset,limit=limit)

@router.get("/{album_id}", response_model=AlbumPDData)
async def get_album(
    album_id: int = Path(..., ge=1),
    album_service: AlbumService = Depends(album_service_dep)   
):
    album = album_service.get_album(album_id)
    if not album:
        raise HTTPException(status_code=404, detail=f"Альбом с id = {album_id} не найден!")
    return album

@router.post("/", response_model=AlbumPD, dependencies=[Depends(security.access_token_required)])
async def add_album(
    album_data: AlbumCreate, 
    album_service: AlbumService = Depends(album_service_dep)
):
    return album_service.create_album(album_data)

@router.put("/{album_id}", response_model=Optional[AlbumPD], dependencies=[Depends(security.access_token_required)])
async def edit_album(
    album_id: int, 
    album_data: AlbumUpdate,
    album_service: AlbumService = Depends(album_service_dep)
):
    return album_service.update_album(album_id, album_data)

@router.delete("/{album_id}", dependencies=[Depends(security.access_token_required)])
async def remove_album(
    album_id: int,  
    album_service: AlbumService = Depends(album_service_dep)
) -> Dict[str, str]:
    if not album_service.delete_album(album_id):
        raise HTTPException(status_code=404, detail=f"Album with id = {album_id} not found!")
    return {"message": f"Album with id = {album_id} was delited"}

@router.get("/search/by-genre/{genre_id}", response_model=List[AlbumPDData])
async def find_albums_by_genre(
    genre_id: int, 
    offset: int = 0, 
    limit: int = 1000,  
    album_service: AlbumService = Depends(album_service_dep)
):
    return album_service.get_albums_genre(genre_id, limit=limit, offset=offset)
