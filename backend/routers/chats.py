from fastapi import APIRouter,HTTPException,Depends,Query
from datetime import date
from typing import Literal
from backend import database as db
from sqlmodel import Session
from backend.entities import chatCollection,Chat,chatCreate,Message,messageCreate,UserCollection,ChatResponse,MessagesResponse,MessageResponse,UserInDB
from backend.auth import get_current_user
from typing import List


chat_router = APIRouter(prefix="/chats",tags=["Chats"])

@chat_router.get("",response_model=chatCollection,description="this api call gets all the chats")
def get_chats(session: Session = Depends(db.get_session)):
    chats=db.get_all_chats(session)
    return chatCollection( meta={"count":len(chats)} , chats=chats)

@chat_router.put("/{chat_id}",response_model = ChatResponse ,description="this api call changes the name of the particular chat witht the given name or if the chat does not exists then raises 404")
def create_user(chat_create: chatCreate,chat_id:int,session: Session = Depends(db.get_session)):
    return db.put_chat(session,chat_id,chat_create)


@chat_router.get("/{chat_id}/messages",response_model=MessagesResponse,description="gets the messages for the particular chat id ")
def get_chat_messages(chat_id:str,session: Session = Depends(db.get_session)):
    return db.get_messages(session,chat_id)


@chat_router.get("/{chat_id}/users",response_model=UserCollection ,description="gets all the users for the given chat id")
def get_chat_user(chat_id:str,session: Session = Depends(db.get_session)):
    return db.get_chat_users(session,chat_id)

@chat_router.post("/{chat_id}/messages",response_model =MessageResponse)
def putChatMessage(chat_id:str,message:messageCreate ,user: UserInDB = Depends(get_current_user),session :Session =  Depends(db.get_session)):
    return db.updateChat(session,chat_id,user,message.text)

@chat_router.get("/{chat_id}")
def getChat(chat_id:str,session :Session =  Depends(db.get_session),include: List[str] =Query(None)):
    return db.getChat(chat_id,session,include)
