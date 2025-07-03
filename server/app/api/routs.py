from typing                        import List

from fastapi                       import APIRouter
from fastapi.params                import Depends

from app.api.auth                  import api as auth
from app.api.users                 import api as register
from app.api.todo                  import api as todo


def get_app_router() -> APIRouter:
    """ Собирает все роуты для приложения в один список и возвращает их """

    api_dependencies: List[Depends] = []
    api_router                      = get_api_router()
    app_router                      = APIRouter()
    app_router.include_router(api_router, dependencies = api_dependencies)

    return app_router


def get_api_router() -> APIRouter:
    """ Собирает все роуты в одну точку """

    api_router       = APIRouter()

    router_auth     = auth.get_router()
    router_register = register.get_router()
    router_pass      = todo.get_router()

    api_router.include_router(router_auth, prefix="/auth", tags=["Аутентификация и авторизация"])
    api_router.include_router(router_register, prefix="/register", tags=["Регистрация пользователя"])
    api_router.include_router(router_pass, prefix="/list", tags=["Список заданий"])

    return api_router
