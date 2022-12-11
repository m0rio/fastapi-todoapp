from fastapi import APIRouter, Request, Response, HTTPException, Depends
from schemas import Todo, TodoBody, SuccessMsg
from fastapi.encoders import jsonable_encoder
from database import db_create_todo, db_get_todos, db_get_single_todo, db_update_todo, db_delete_todo
from starlette.status import HTTP_201_CREATED
import uuid
from typing import List
from fastapi_csrf_protect import CsrfProtect
from auth_utils import AuthJwtCsrf

#インスタンス作成
router = APIRouter()
auth = AuthJwtCsrf()

@router.get("/", response_model=SuccessMsg)
def root():
    return {"message": "world"}

@router.post("/api/todo", response_model=Todo)
def create_todo(request: Request, response: Response, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
    # CSRF TokenとJWTが有効か検証する
    new_token = auth.verify_csrf_update_jwt(request, csrf_protect,request.headers)
    # json -> dictに変更
    todo = jsonable_encoder(data)
    id = str(uuid.uuid4())
    todo["id"] = id
    res = db_create_todo(todo)
    # ステータスコードを上書き
    response.status_code = HTTP_201_CREATED
    # JWTを新しい値に更新
    response.set_cookie(
        key="access_token", value=f"Bearer {new_token}", httponly=True, samesite=None, secure=True)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail="Create task failed"
    )

@router.get("/api/todo", response_model=List[Todo])
def get_todos(request: Request):
    # JWTを検証
    auth.verify_jwt(request)
    res = db_get_todos()
    print(res)
    return res

@router.get("/api/todo/{id}", response_model=Todo)
def get_single_todo(id: str, request: Request, response: Response):
    new_token, _ = auth.verify_update_jwt(request)
    res = db_get_single_todo(id)
    response.set_cookie(
        key="access_token", value=f"Bearer {new_token}", httponly=True, samesite=None, secure=True)
    if res:
        return res
    return HTTPException(
        status_code=404,
        detail=f"Task of ID:{id} doesn't exit"
        )

@router.put("/api/todo/{id}", response_model=Todo)
def update_todo(request: Request, response: Response, id: str, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
    # CSRF TokenとJWTが有効か検証する
    new_token = auth.verify_csrf_update_jwt(request, csrf_protect,request.headers)
    todo = jsonable_encoder(data)
    res = db_update_todo(id, todo)
    response.set_cookie(
        key="access_token", value=f"Bearer {new_token}", httponly=True, samesite=None, secure=True)
    if res:
        return res
    return HTTPException(
        status_code=404,
        detail=f"Update Task failed"
        )

@router.delete("/api/todo/{id}", response_model=SuccessMsg)
def delete_todo(request: Request, response: Response, id: str, csrf_protect: CsrfProtect = Depends()):
    # CSRF TokenとJWTが有効か検証する
    new_token = auth.verify_csrf_update_jwt(request, csrf_protect,request.headers)
    res = db_delete_todo(id)
    response.set_cookie(
        key="access_token", value=f"Bearer {new_token}", httponly=True, samesite=None, secure=True)
    if res:
        return {"message": "Successfully deleted"}
    return False

