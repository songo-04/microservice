from fastapi import APIRouter, status, HTTPException, Depends
from bson import ObjectId

from utils.is_auth import is_authenticate
from models.private_message_model import (
    PrivateMessageModel,
    decode_message_private,
    decode_message_private_list,
)
from config.config import private_message_collection


message_private_router = APIRouter(prefix="/api/messagerie/private")


@message_private_router.get("/")
async def get():
    return {"message": status.HTTP_200_OK}


@message_private_router.post("/{_id}")
async def send_message(
    _id: str, data: PrivateMessageModel, is_auth: dict = Depends(is_authenticate)
):
    userId = is_auth["userId"]
    new_message = PrivateMessageModel(
        sender_id=userId, receiver_id=str(ObjectId(_id)), messages=data.messages
    )
    print(userId)
    private_message_collection.insert_one(dict(new_message))
    return {"message": status.HTTP_201_CREATED, "userId": userId, "receiver_id": _id}


@message_private_router.get("/{_id}")
async def get_message(_id: str, is_auth: dict = Depends(is_authenticate)):
    userId = is_auth["userId"]
    data = private_message_collection.find(
        {
            "$or": [
                {"sender_id": userId, "receiver_id": _id},
                {"sender_id": _id, "receiver_id": userId},
            ]
        }
    )
    data = decode_message_private_list(data)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, details="messages not found"
        )
    return data


@message_private_router.delete("/{_id}/{_id_message}")
async def delete_message(
    _id: str, _id_message: str, is_auth: dict = Depends(is_authenticate)
):
    userId = is_auth["userId"]
    is_message_exist = private_message_collection.find_one(
        {
            "_id": ObjectId(_id_message),
            "$or": [
                {"sender_id": userId, "receiver_id": _id},
                {"sender_id": _id, "receiver_id": userId},
            ],
        }
    )
    if is_message_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, details="message not found"
        )
    private_message_collection.delete_one(
        {
            "_id": ObjectId(_id_message),
            "$or": [
                {"sender_id": userId, "receiver_id": _id},
                {"sender_id": _id, "receiver_id": userId},
            ],
        }
    )
    return {"message": status.HTTP_200_OK}
