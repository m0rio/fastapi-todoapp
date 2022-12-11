from decouple import config
import boto3
from typing import Union
from auth_utils import AuthJwtCsrf
from fastapi import HTTPException

# リソース API を使うとき
dynamodb = boto3.resource("dynamodb")
# クライアント API を使うとき
dynamodb_client = boto3.client("dynamodb")
# todo テーブルを参照する
todo_table = boto3.resource("dynamodb").Table("todo")
# user テーブルを参照する
user_table = boto3.resource("dynamodb").Table("user")

# AuthJwtCsrfクラスのインスタンス作成
auth = AuthJwtCsrf()


def db_create_todo(data: dict) -> Union[dict, bool]:
    id = data["id"]
    print(id)
    response = todo_table.get_item(Key={"id": id})
    todo_table.put_item(Item = data)
    if "Item" in response:
        return False
    # 新規登録に成功した場合は登録したデータを返却
    return {
        "id": str(data["id"]),
        "title": data["title"],
        "description": data["description"]
    }

def db_get_todos() -> list:
    todos = []
    response = todo_table.scan()
    print(response)
    for item in response["Items"]:
        print(item)
        todos.append(item)
    print(todos)
    return todos

def db_get_single_todo(id: str) -> Union[dict, bool]:
    response = todo_table.get_item(Key={"id": id})
    print(response)
    if response:
        return response["Item"]
    return False

def db_update_todo(id: str, data: dict) -> bool:
    res = todo_table.get_item(Key={"id": id})
    if res:
        data["id"] = id
        todo_table.put_item(Item = data)
        return data
    return False

def db_delete_todo(id: str) -> bool:
    res = todo_table.delete_item(Key={'id': id})
    if res:
        return True
    return False

def db_signup(data: dict) -> dict:
    email = data.get("email")
    password = data.get("password")
    overwrap_user = user_table.get_item(Key={"email": email})
    if "Item" in overwrap_user:
        raise HTTPException(status_code=400, detail="Email is already taken")
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Password too short")
    data["password"] = auth.generate_hashed_pw(password)
    res = user_table.put_item(Item = data)
    print(res)
    return data

def db_login(data: dict) -> str:
    email = data.get("email")
    password = data.get("password")
    user = user_table.get_item(Key={"email": email})
    if not user or not auth.verify_pw(password, user.get("Item").get("password")):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = auth.encode_jwt(user.get("Item").get("email"))
    return token