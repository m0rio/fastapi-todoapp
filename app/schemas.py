# 型を定義するclass

from pydantic import BaseModel

# req
class TodoBody(BaseModel):
    title: str
    description: str

# res
class Todo(BaseModel):
    id: str
    title: str
    description: str