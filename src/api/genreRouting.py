from fastapi import APIRouter, HTTPException, Depends
from src.bd.database import session_factory
from src.models.modelsPD import GenreBase, GenrePD, GenreCreate, GenrePDData
from typing import List, Dict
from src.core.security import security
from src.service.genre import GenreService
from src.core.depends import genre_service_dep


router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)


@router.get("/", response_model=List[GenreBase])
async def get_genres(
    limit: int = 1000,
    offset: int = 0,
    genre_service: GenreService = Depends(genre_service_dep),
):
    return genre_service.get_genres(offset, limit)


@router.get(
    "/{id_genre}",
    response_model=GenrePDData,
    dependencies=[Depends(security.access_token_required)],
)
async def find_genre_by_id(
    id_genre: int,
    genre_service: GenreService = Depends(genre_service_dep),
):
    genre = genre_service.get_genre(id_genre)
    if not genre:
        raise HTTPException(status_code=404, detail=f"Genre with id = {id_genre} not found!")
    return genre


@router.post(
    "/", response_model=GenrePD, dependencies=[Depends(security.access_token_required)]
)
async def create_genre(
    data: GenreCreate,
    genre_service: GenreService = Depends(genre_service_dep),
):
    return genre_service.create_genre(data)


@router.delete("/", response_model=Dict[str, str])
async def remove_genre(
    genre_id: int,
    genre_service: GenreService = Depends(genre_service_dep),
):
    if not genre_service.delete(genre_id):
        raise HTTPException(status_code=404, detail=f"Genre with id = {genre_id} not found!")
    return {"Message": "Ok"}
