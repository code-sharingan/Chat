from fastapi import APIRouter,HTTPException
from datetime import date
from typing import Literal
from backend import database as db
from backend.entities import chatCollection,Chat

chat_router = APIRouter(prefix="/chats",tags=["chats"])

@chat_router.get("",response_model=chatCollection)
def get_chats():
    sort_key =lambda Chat: Chat.name
    chat_list = db.get_all_chats()
    return chatCollection(
        meta={"count":len(chat_list)},
        chats =sorted(chat_list,key=sort_key))
