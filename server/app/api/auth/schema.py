from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    login: str = Field(...)
    password: str = Field(...)

class UserAuth(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)

class UserAccess(UserAuth):
    refresh_token: None = Field(None)

class UserName(BaseModel):
    name: str = Field(...)
    status: str = Field(...)