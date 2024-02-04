from fastapi import APIRouter,HTTPException
from datetime import date
from typing import Literal
from backend import database as db
from backend.entities import chatCollection,Chat,chatIDB,chatCreate,messagesIDB,Message,UserCollection

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

@chat_router.delete("/{chat_id}",response_model=None,status_code=204)
def delete_chat(chat_id:str):
    db.del_chat(chat_id)

@chat_router.get("/{chat_id}/messages",response_model=messagesIDB)
def get_chat_messages(chat_id:str):
    messages =db.get_messages(chat_id)
    return messagesIDB(meta={"count":len(messages)} , messages=messages)


@chat_router.get("/{chat_id}/users",response_model=UserCollection)
def get_chat_user(chat_id:str):
    user = db.get_chat_user(chat_id)
    return UserCollection(meta={"count":len(user)} , users=user)

