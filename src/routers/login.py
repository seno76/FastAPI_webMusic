import hashlib
from fastapi import APIRouter, Response, HTTPException, Depends
from src.schemas import UserLogin
from src.core.security import security
from src.repository.userRepository import UserRepository
from src.bd.database import session_factory
from src.service.user import UserService
from src.core.depends import user_service_dep


router = APIRouter(
    prefix="/login",
    tags=["Login"]
)


@router.post('')
def login(
    data: UserLogin,
    response: Response,
    user_service: UserService = Depends(user_service_dep),
):
    login = data.username
    passwd_byte = data.password_hash.encode('utf-8')
    passwd = hashlib.sha256(passwd_byte).hexdigest()
    print(passwd)
    if user_service.login_user(login, passwd):
        token = security.create_access_token(uid=data.username)
        response.set_cookie("token", token)
        csrf = security.create_refresh_token(uid=data.username)
        response.set_cookie("csrf_token", csrf)
        return {"access_token": token}
    raise HTTPException(401, detail={"message": "Bad credentials"})


@router.get("/protected", dependencies=[Depends(security.access_token_required)])
def get_protected():
    return {"message": "Hello World"}


@router.post("/logout")
async def logout(response: Response):
    # AuthX предоставляет удобные методы для очистки
    security.unset_cookies(response)

    return {"message": "Successfully logged out"}
