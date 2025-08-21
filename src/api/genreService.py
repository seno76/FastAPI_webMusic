from fastapi import APIRouter, HTTPException
from src.bd.database import session_factory
from src.models.modelsPD import GenreBase, GenrePD, GenreCreate, GenrePDData
from typing import List, Dict
from src.repository.genreRepository import (
    get_all_genres,
    get_genre_by_id,
    create_new_genre,
    delete_genre,
)


router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)

@router.get("/", response_model=List[GenreBase])
async def get_genres(limit: int = 1000, offset: int = 0):
    return get_all_genres(session_factory, offset, limit)

@router.get("/{id_genre}", response_model=GenrePDData)
async def find_genre_by_id(id_genre: int):
    genre = get_genre_by_id(session_factory, id_genre)
    if not genre:
        raise HTTPException(status_code=404, detail=f"Genre with id = {id_genre} not found!")
    return get_genre_by_id(session_factory, id_genre)

@router.post("/", response_model=GenrePD)
async def create_genre(data: GenreCreate):
    return create_new_genre(session_factory, data)


@router.delete("/", response_model=Dict[str, str])
async def remove_genre(genre_id: int):
    if not delete_genre(session_factory, genre_id):
        raise HTTPException(status_code=404, detail=f"Genre with id = {genre_id} not found!")
    return {"Message": "Ok"}