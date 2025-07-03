from fastapi             import APIRouter, HTTPException, Depends, status
from typing              import Dict

from app.api.todo.models import Todo, data_pydantic, data_pydanticIn

from app.api.auth.models  import Authentification


router   = APIRouter()

@router.get("/todo")
async def get_all_todo(token: Dict = Depends(Authentification.get_current_user)):
    """ Получаем все задачи """

    stat     = token["status"]

    if stat == "block":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы были заблокированы обратитесь в поддержку")

    role     = token["role"]
    token_id = token["id"]

    try:
        todos     = await Todo.filter(user_id=token_id, user_role=role).all()
        response = [data_pydantic.from_orm(todo) for todo in todos]

        return {"Your todos": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")


@router.post("/todo")
async def add_todo(todo_info: data_pydanticIn, token: Dict = Depends(Authentification.get_current_user)):
    """ Добавляем задачу """

    stat              = token["status"]

    if stat == "block":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы были заблокированы обратитесь в поддержку")

    role              = token["role"]
    token_id          = token["id"]

    data              = todo_info.dict(exclude_unset=True)
    data["user_id"]   = token_id
    data["user_role"] = role

    try:
        todo_obj  = await Todo.create(**data)
        response  = await data_pydantic.from_tortoise_orm(todo_obj)

        return {"status": "ok", "data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")


@router.put("/todo/{todo_id}")
async def update_todo(todo_id: int, update_todo: data_pydanticIn, token: Dict = Depends(Authentification.get_current_user)):
    """ Редактируем задачу """

    stat = token["status"]

    if stat == "block":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы были заблокированы обратитесь в поддержку")

    data = await Todo.get_or_none(id=todo_id, user_id=token["id"], user_role=token["role"])

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой записи не существует")

    try:
        update_todo           = update_todo.dict(exclude_unset = True)
        data.todo_name        = update_todo['todo_name']
        data.todo_description = update_todo['todo_description']
        data.todo_date_time   = update_todo['todo_date_time']
        await data.save()

        response              = await data_pydantic.from_tortoise_orm(data)

        return {"status": "ok", "data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")


@router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, token: Dict = Depends(Authentification.get_current_user)):
    """ Удаляем задачу """

    stat = token["status"]

    if stat == "block":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы были заблокированы обратитесь в поддержку")

    data = await Todo.get_or_none(id=todo_id, user_id=token["id"], user_role=token["role"])

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой записи не существует")

    try:
        await data.delete()

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")

def get_router() -> APIRouter:
    """ Возвращает роутеры """

    return router
