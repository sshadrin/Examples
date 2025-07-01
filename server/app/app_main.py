import logging

from fastapi                                 import FastAPI

from app.api.routs                           import get_app_router
from app.fast_api_settings.util_settings     import setup_openapi, setup_cors
from app.fast_api_settings.api_settings      import APISettings

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    """ функция фабрика. Создает и конфигурирует сервер. """

    api_settings = APISettings()
    server       = FastAPI(**api_settings.fastapi_kwargs())
    add_routes(server, api_settings.main_router_prefix)
    setup_openapi(server)
    setup_cors(server)

    return server


def add_routes(server: FastAPI, router_prefix: str) -> None:
    """ Добавляем роуты """

    app_router = get_app_router()
    server.include_router(app_router, prefix = router_prefix)