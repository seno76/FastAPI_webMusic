from src.bd.database import session_factory, sync_engine
from src.models.modelsPD import *
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from src.repository.userRepository import (
    get_user_by_id_orm,
    get_users_is_active,
    get_user_by_username,
    get_user_by_email,
    get_count_users,
    set_user_status,
)
from typing import List, Optional

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/active", response_model=List[UserPDData])
async def get_active_users() -> List[UserPDData]:
    return get_users_is_active(session_factory)

# 3. Получить пользователя по имени
@router.get("/by-username/{username}", response_model=UserPDData)
async def get_user_by_name(username: str) -> UserPDData:
    user = get_user_by_username(session_factory, username)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Пользователь {username} не найден")
    return user


# 4. Получить пользователя по email
@router.get("/by-email/{email}", response_model=UserPDData)
async def get_user_by_email_route(email: str) -> UserPDData:
    user = get_user_by_email(session_factory, email)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с email {email} не найден")
    return user

# 8. Получить количество пользователей
@router.get("/count", response_model=int)
async def count_users(only_active: Optional[bool] = Query(None)):
    return get_count_users(session_factory, only_active)

# 6. Изменить статус пользователя (активен/не активен)
@router.put("/{id_user}/status", response_model=UserPDData)
async def change_user_status(
    id_user: int,
    status: bool = Query(..., description="True — активен, False — деактивирован"),
) -> UserPDData:
    updated_user = set_user_status(session_factory, id_user, status)
    if updated_user is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с id={id_user} не найден")
    return updated_user

@router.get("/{id_user}", response_model=UserPDData)
async def get_user_by_id(id_user: int = Path(description="ID пользователя")) -> UserPDData:
    return get_user_by_id_orm(session_factory, id_user)




