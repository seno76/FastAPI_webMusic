import hashlib
from fastapi import APIRouter, Response, HTTPException, Depends
from src.models.modelsPD import UserLogin
from src.core.security import security
from src.repository.userRepository import auth_user
from src.bd.database import session_factory



router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post('')
def login(data: UserLogin, response: Response):
    login = data.username
    passwd_byte = data.password_hash.encode('utf-8')
    passwd = hashlib.sha256(passwd_byte).hexdigest()
    print(passwd)
    if auth_user(session_factory, login, passwd):
        token = security.create_access_token(uid=data.username)
        response.set_cookie("token", token)
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
