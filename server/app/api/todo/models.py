from tortoise                  import Model
from tortoise                  import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class Todo(Model):
    """ Формируем модель данных в БД """

    id               = fields.IntField(pk=True)
    user_id          = fields.IntField(max_length=3, nullable=False)
    user_role        = fields.CharField(max_length=5, nullable=False)
    todo_name        = fields.CharField(max_length=100, nullable=False)
    todo_description = fields.CharField(max_length=100, nullable=False)
    todo_date_time   = fields.DateField()


data_pydantic = pydantic_model_creator(Todo, name="Todo")
data_pydanticIn = pydantic_model_creator(Todo, name="TodoIn", exclude=("user_id", "user_role"), exclude_readonly=True)