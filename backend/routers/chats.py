from fastapi import APIRouter,HTTPException
from datetime import date
from typing import Literal
from backend import database as db
from backend.entities import chatCollection,Chat,chatIDB,chatCreate

chat_router = APIRouter(prefix="/chats",tags=["chats"])

@chat_router.get("",response_model=chatCollection)
def get_chats():
    sort_key =lambda Chat: Chat.name
    chat_list = db.get_all_chats()
    return chatCollection(
        meta={"count":len(chat_list)},
        chats =sorted(chat_list,key=sort_key))

@chat_router.get("/{chat_id}" , response_model=chatIDB)
def get_caht(chat_id:str):
    chat =db.get_chat(chat_id)
    return chatIDB(chat=chat)

@chat_router.post("/{chat_id}",response_model = chatIDB)
def create_user(chat_create: chatCreate,chat_id:str):
    return chatIDB(chat=db.put_chat(chat_id,chat_create))