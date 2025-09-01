from fastapi import APIRouter, HTTPException, Path, Query, Depends
from typing import List, Optional
from src.models.modelsPD import AuthorPDData, AuthorUpdate, AuthorCreate
from src.core.security import security
from src.core.depends import author_service_dep
from src.service.author import AuthorService

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get(
    "/",
    response_model=List[AuthorPDData],
    dependencies=[Depends(security.access_token_required)],
)
async def list_authors(
    author_service: AuthorService = Depends(author_service_dep),
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=10000),
) -> List[AuthorPDData]:
    return author_service.get_authors(offset, limit)


@router.get(
    "/{author_id}",
    response_model=AuthorPDData,
    dependencies=[Depends(security.access_token_required)],
)
async def get_author(
    author_id: int = Path(..., description="ID автора"),
    author_service: AuthorService = Depends(author_service_dep),
) -> AuthorPDData:
    author = author_service.get_author(author_id)
    if not author:
        raise HTTPException(status_code=404, detail=f"Автор с id={author_id} не найден")
    return author


@router.get(
    "/by-user/{user_id}",
    response_model=AuthorPDData,
    dependencies=[Depends(security.access_token_required)],
)
async def get_author_by_user(
    user_id: int,
    author_service: AuthorService = Depends(author_service_dep),
) -> AuthorPDData:
    author = author_service.get_author_by_user_id(user_id)
    if not author:
        raise HTTPException(status_code=404, detail=f"Автор с user_id={user_id} не найден")
    return author


@router.post(
    "/",
    response_model=AuthorPDData,
    dependencies=[Depends(security.access_token_required)],
)
async def create_author(
    data: AuthorCreate,
    author_service: AuthorService = Depends(author_service_dep),
) -> AuthorPDData:
    try:
        return author_service.create_author(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{author_id}",
    response_model=AuthorPDData,
    dependencies=[Depends(security.access_token_required)],
)
async def update_author_data(
    author_id: int,
    data: AuthorUpdate,
    author_service: AuthorService = Depends(author_service_dep),
) -> AuthorPDData:
    updated_author = author_service.update_author(author_id, data)
    if not updated_author:
        raise HTTPException(status_code=404, detail=f"Автор с id={author_id} не найден")
    return updated_author


@router.delete("/{author_id}", dependencies=[Depends(security.access_token_required)])
async def delete_author(
    author_id: int,
    author_service: AuthorService = Depends(author_service_dep),
):
    author_service.delete_author(author_id)
    return {"status": "ok", "message": f"Автор с id={author_id} удалён"}
