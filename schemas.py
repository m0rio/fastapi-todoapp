# データ型を定義するclass

from pydantic import BaseModel
from typing import Optional
from decouple import config

CSRF_KEY = config("CSRF_KEY")

class CsrfSettings(BaseModel):
  secret_key:str = CSRF_KEY

# req
class TodoBody(BaseModel):
    title: str
    description: str

# res
class Todo(BaseModel):
    id: str
    title: str
    description: str

# レスポンスで返すメッセージ
class SuccessMsg(BaseModel):
    message: str

class UserBody(BaseModel):
    email: str
    password: str

class UserInfo(BaseModel):
    # id: Optional[str] = None
    email: str

class Csrf(BaseModel):
    csrf_token: str