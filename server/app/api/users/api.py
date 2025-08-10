from fastapi              import APIRouter, HTTPException, Depends, status

from typing               import Dict

from app.api.users.models import Admin, BaseUser, admin_pydantic, admin_pydanticIn, user_base_pydantic, user_base_pydanticIn
from app.api.auth.models  import Authentification


router   = APIRouter()

@router.post("/register_admin")
async def register_admin(register: admin_pydanticIn):
    """ регистрация админа """

    exist_name = await Admin.get_or_none(user_name=register.user_name)

    if exist_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )

    data              = register.dict(exclude_unset=True)
    data['user_pass'] = Authentification.hash_password(data['user_pass'])

    try:
        register_admin = await Admin.create(**data)
        response       = await admin_pydantic.from_tortoise_orm(register_admin)

        return {"status": "200", "data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")


@router.post("/register_user")
async def register_user(register: user_base_pydanticIn):
    """ регистрация пользователя """

    exist_name = await BaseUser.get_or_none(user_name=register.user_name)

    if exist_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )

    data              = register.dict(exclude_unset=True)
    data['user_pass'] = Authentification.hash_password(data['user_pass'])

    try:
        register_user = await BaseUser.create(**data)
        response      = await user_base_pydantic.from_tortoise_orm(register_user)

        return {"status": "200", "data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")


@router.get("/get_users")
async def get_all_users(token: Dict = Depends(Authentification.get_current_user)):
    """ Получаем всех пользователей """

    role = token["role"]

    if role == "admin":
        try:
            response_admin  = await admin_pydantic.from_queryset(Admin.all())
            response_users  = await user_base_pydantic.from_queryset(BaseUser.all())

            return {"Admins": response_admin, "Users": response_users}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ ограничен")


@router.put("/block_user/{user_id}")
async def block_user(user_id: int, token: Dict = Depends(Authentification.get_current_user)):
    """ Заблокировать пользователя """

    role = token["role"]

    if role == "admin":
        data = await BaseUser.get_or_none(id=user_id)

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой записи не существует")

        try:
            data.user_status          = "block"
            await data.save()

            response                  = await user_base_pydantic.from_tortoise_orm(data)

            return {"status": "ok", "data": response}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ ограничен")


@router.put("/unblock_user/{user_id}")
async def unblock_user(user_id: int, token: Dict = Depends(Authentification.get_current_user)):
    """ Разблокировать пользователя """

    role = token["role"]

    if role == "admin":
        data = await BaseUser.get_or_none(id=user_id)

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой записи не существует")

        try:
            data.user_status          = "active"
            await data.save()

            response                  = await user_base_pydantic.from_tortoise_orm(data)

            return {"status": "ok", "data": response}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ ограничен")


@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, token: Dict = Depends(Authentification.get_current_user)):
    """ Удаляем пользователя """

    role = token["role"]

    if role == "admin":

        data = await BaseUser.get_or_none(id=user_id)

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой записи не существует")

        try:
            await data.delete()

            return {"status": "ok"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ ограничен")


def get_router() -> APIRouter:
    """ Возвращает роутеры """

    return router
