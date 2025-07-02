from fastapi             import APIRouter, HTTPException

from app.api.todo.models import Todo, data_pydantic, data_pydanticIn


router   = APIRouter()

@router.get("/todo")
async def get_all_todo():
    """ Получаем все задачи """

    try:
        response  = await data_pydantic.from_queryset(Todo.all())

        return {"Your todos": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")


@router.post("/todo")
async def add_todo(todo_info: data_pydanticIn):
    """ Добавляем задачу """

    try:
        todo_obj  = await Todo.create(**todo_info.dict(exclude_unset = True))
        response  = await data_pydantic.from_tortoise_orm(todo_obj)

        return {"status": "ok", "data": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")


@router.put("/todo/{todo_id}")
async def update_todo(todo_id: int, update_todo: data_pydanticIn):
    """ Редактируем задачу """

    try:
        data                  = await Todo.get(id = todo_id)
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
async def delete_todo(todo_id: int):
    """ Удаляем задачу """

    try:
        data = await Todo.get(id = todo_id)
        if data:
            await data.delete()

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"База данных не отвечает: {e}")

def get_router() -> APIRouter:
    """ Возвращает роутеры """

    return router
