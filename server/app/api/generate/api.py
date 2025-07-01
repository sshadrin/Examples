from fastapi import APIRouter, HTTPException

from app.api.generate.schema import GetPass, GetPassParam
from app.api.generate.models import PassGenerate

router = APIRouter()

@router.post("/path", response_model=GetPass, summary="Генерация пароля")
async def generate(param: GetPassParam) -> GetPass:

    if param.length <= 0 or param.length > 50:
        raise HTTPException(status_code=400, detail="Пароль должен содержать от 1 до 50 символов")

    if type(param.length) is not int:
        raise HTTPException(status_code=400, detail="Введите корректную длину пароля")

    generate_pass = await PassGenerate.generate(param.length, param.low_str, param.hight_str, param.symbol, param.number)

    return generate_pass


def get_router() -> APIRouter:
    """ Возвращает роутеры """

    return router
