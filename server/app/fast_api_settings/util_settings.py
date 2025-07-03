from fastapi                 import FastAPI
from fastapi.routing         import APIRoute
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI) -> None:
    """ Устанавливает разрешенные адреса для запросов """

    origins = [
        "http://localhost:3000",
        "localhost:3000",
        'http://localhost:3000',
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def setup_openapi(app: FastAPI) -> None:
    """ Упрощает идентификаторы операций, чтобы сгенерированные клиенты имели более простые имена функций API """

    for route in app.routes:
        if isinstance(route, APIRoute): route.operation_id = route.name