from tortoise                  import Model
from tortoise                  import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class AbstractUser(Model):
    """ Формируем абстрактную модель данных для всех пользователей """

    id               = fields.IntField(pk=True)
    user_name        = fields.CharField(max_length=100, nullable=False)
    user_pass        = fields.CharField(max_length=300, nullable=False)
    user_date_create = fields.DateField()

    class Meta:
        abstract = True

class Admin(AbstractUser):
    """ Модель админа в БД """

    user_role    = fields.CharField(max_length=5, nullable=False, default="admin")


class BaseUser(AbstractUser):
    """ Модель пользователя добавляет поля статус и баланс в БД """

    user_status  = fields.CharField(max_length=10, nullable=False, default="active")
    user_role    = fields.CharField(max_length=4, nullable=False, default="base")


admin_pydantic       = pydantic_model_creator(Admin, name="Admin")
admin_pydanticIn     = pydantic_model_creator(Admin, name="Admin_In", exclude=("user_role",), exclude_readonly=True)

user_base_pydantic   = pydantic_model_creator(BaseUser, name="Base_user")
user_base_pydanticIn = pydantic_model_creator(BaseUser, name="Base_user_In", exclude=("user_role", "user_status"), exclude_readonly=True)