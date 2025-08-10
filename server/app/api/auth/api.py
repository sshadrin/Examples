import bcrypt

from   fastapi              import APIRouter, HTTPException, status, Depends
from   fastapi.security     import APIKeyHeader

from   typing               import Dict

from   app.api.auth.models  import Authentification
from   app.api.users.models import Admin, BaseUser
from   app.api.auth.schema  import UserAuth, UserLogin, UserAccess, UserName

router  = APIRouter()

api_key_header = APIKeyHeader(name="Authorization")

@router.post("/token", response_model=UserAuth, summary="Получение токена")
async def token(user: UserLogin) -> UserAuth:
    admin         = await Admin.get_or_none(user_name=user.login)
    user_data     = await BaseUser.get_or_none(user_name=user.login)
    auth          = Authentification()

    if admin and bcrypt.checkpw(user.password.encode('utf-8'), admin.user_pass.encode('utf-8')):
        access_token  = auth.create_access_token(data={
            "sub"   : admin.user_name,
            "id"    : admin.id,
            "role"  : admin.user_role,
            "status": "active",
        })
        refresh_token = auth.create_refresh_token(data={
            "sub"   : admin.user_name,
            "id"    : admin.id,
            "role"  : admin.user_role,
            "status": "active",
        })

        return UserAuth(access_token=access_token, refresh_token=refresh_token)

    if user_data and bcrypt.checkpw(user.password.encode('utf-8'), user_data.user_pass.encode('utf-8')):
        access_token = auth.create_access_token(data={
            "sub"   : user_data.user_name,
            "id"    : user_data.id,
            "role"  : user_data.user_role,
            "status": user_data.user_status,
        })
        refresh_token = auth.create_refresh_token(data={
            "sub"   : user_data.user_name,
            "id"    : user_data.id,
            "role"  : user_data.user_role,
            "status": user_data.user_status,
        })

        return UserAuth(access_token=access_token, refresh_token=refresh_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/refresh", response_model=UserAccess, summary="Обновление токена")
async def Refresh(token: Dict = Depends(Authentification.get_current_user_refresh)) -> UserAccess:
    auth = Authentification()

    # Генерация нового access токена
    new_access_token = auth.create_access_token(data={
        "sub"   : token["username"],
        "id"    : token["id"],
        "role"  : token["role"],
        "status": token["status"],
    })

    return UserAccess(access_token=new_access_token)


@router.get("/check", response_model=UserName, summary="Проверяем токен")
async def Check(token: Dict = Depends(Authentification.get_current_user)) -> UserName:
    return UserName(name=token["username"], status="Token is valid")


def get_router() -> APIRouter:
    """ Возвращает роутеры """
    return router