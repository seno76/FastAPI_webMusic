from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import List, Optional
from fastapi.background import P
from src.schemas import UserPD, UserPDData, UserCreate, PlayListPDData
from src.core.depends import user_service_dep
from src.service.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserPD])
async def get_users(
    user_service: UserService = Depends(user_service_dep),
) -> List[UserPD]:
    users = user_service.get_users()
    return users


@router.get("/count", response_model=int)
async def count_users(
    user_service: UserService = Depends(user_service_dep),
    only_active: Optional[bool] = Query(None),
):
    return user_service.count_users(only_active)


@router.post("/create", response_model=UserPDData)
async def create_new_user(
    data: UserCreate,
    user_service: UserService = Depends(user_service_dep),
) -> UserPDData:
    return user_service.create_user(data)


@router.get("/{user_id}/playlists", response_model=List[PlayListPDData])
async def get_playlist_for_user(
    user_id: int,
    user_service: UserService = Depends(user_service_dep),
) -> List[PlayListPDData]:
    return user_service.get_playlist(user_id)


@router.get("/{user_id}", response_model=UserPDData)
async def find_user_by_id(
    user_id: int = Path(..., description="ID пользователя"),
    user_service: UserService = Depends(user_service_dep),
) -> UserPDData:
    return user_service.get_user(user_id)


@router.get("/active/", response_model=List[UserPD])
async def find_users_is_active(
    user_service: UserService = Depends(user_service_dep),
) -> List[UserPD]:
    return user_service.get_active_users()


@router.get("/passive/", response_model=List[UserPD])
async def find_users_is_passive(
    user_service: UserService = Depends(user_service_dep),
) -> List[UserPD]:
    return user_service.get_passive_users()


@router.get("/by-username/{username}", response_model=UserPDData)
async def find_user_by_name(
    username: str,
    user_service: UserService = Depends(user_service_dep),
) -> UserPDData:
    user = user_service.get_user_by_name(username)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"Пользователь {username} не найден"
        )
    return user


@router.get("/by-email/{email}", response_model=UserPDData)
async def get_user_by_email_route(
    email: str,
    user_service: UserService = Depends(user_service_dep),
) -> UserPDData:
    user = user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с email {email} не найден")
    return user


@router.put("/{id_user}/status", response_model=UserPDData)
async def change_user_status(
    id_user: int,
    user_service: UserService = Depends(user_service_dep),
    status: bool = Query(..., description="True — активен, False — деактивирован"),
) -> UserPDData:
    updated_user = user_service.set_status(id_user, status)
    if updated_user is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с id={id_user} не найден")
    return updated_user


@router.delete("/delete")
async def delete_user(
    id_user: int,
    user_service: UserService = Depends(user_service_dep),
):
    user_service.delete(id_user)
    return {"message": f"Пользователь с id={id_user} удален"}
