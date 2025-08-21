from fastapi import APIRouter, HTTPException, Path, Query, Body
from typing import List, Optional
from src.bd.database import session_factory
from src.models.modelsPD import AuthorPDData, AuthorUpdate, AuthorCreate
from src.repository.authorRepository import (
    get_author_by_id,
    get_by_user_id,
    create_new_author,
    delete_aythor_by_id,
    update_author,
    get_all_authors
)

router = APIRouter(prefix="/authors", tags=["authors"])

# Получить всех авторов
@router.get("/", response_model=List[AuthorPDData])
async def list_authors(offset: int = Query(0, ge=0), limit: int = Query(100, le=10000)) -> List[AuthorPDData]:
    return get_all_authors(session_factory, offset=offset, limit=limit)

# Получить автора по ID
@router.get("/{author_id}", response_model=AuthorPDData)
async def get_author(author_id: int = Path(..., description="ID автора")) -> AuthorPDData:
    author = get_author_by_id(session_factory, author_id)
    if not author:
        raise HTTPException(status_code=404, detail=f"Автор с id={author_id} не найден")
    return author

# Получить автора по ID пользователя
@router.get("/by-user/{user_id}", response_model=AuthorPDData)
async def get_author_by_user(user_id: int) -> AuthorPDData:
    author = get_by_user_id(session_factory, user_id)
    if not author:
        raise HTTPException(status_code=404, detail=f"Автор с user_id={user_id} не найден")
    return author

# Создать нового автора
@router.post("/", response_model=AuthorPDData)
async def create_author(data: AuthorCreate) -> AuthorPDData:
    try:
        return create_new_author(session_factory, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Обновить данные автора
@router.patch("/{author_id}", response_model=AuthorPDData)
async def update_author_data(author_id: int, data: AuthorUpdate) -> AuthorPDData:
    updated_author = update_author(session_factory, author_id, data)
    if not updated_author:
        raise HTTPException(status_code=404, detail=f"Автор с id={author_id} не найден")
    return updated_author

# Удалить автора
@router.delete("/{author_id}")
async def delete_author(author_id: int):
    delete_aythor_by_id(session_factory, author_id)
    return {"status": "ok", "message": f"Автор с id={author_id} удалён"}
