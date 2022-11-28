from fastapi import APIRouter, Request, Response
from schemas import Todo, TodoBody
from fastapi.encoders import jsonable_encoder
from database import db_create_todo
from starlette.status import HTTP_201_CREATED
#インスタンス作成
router = APIRouter

@router.post("/api/todo", response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody):
    # json -> dictに変更
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)
    # ステータスコードを上書き
    response.status_code = HTTP_201_CREATED
    if res:
        return res