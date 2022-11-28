from decouple import config
import boto3

# リソース API を使うとき
dynamodb = boto3.resource("dynamodb")
# クライアント API を使うとき
dynamodb_client = boto3.client("dynamodb")
# Books テーブルを参照する
table = boto3.resource("dynamodb").Table("todo")


async def db_create_todo(data: dict) -> dict:
    response = await table.get_item(Key={"id": data["id"]})
    await table.put_item(Item = data)
    if "Item" in response:
        return False
    # 新規登録の場合は、登録したデータを返却
    return {
        "id": str(data["id"]),
        "title": data["title"],
        "description": data["description"]
    }






