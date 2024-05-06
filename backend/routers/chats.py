from fastapi import APIRouter,HTTPException,Depends,Query
from datetime import date
from typing import Literal
from backend import database as db
from sqlmodel import Session
from backend.entities import chatCollection,Chat,chatCreate,Message,messageCreate,UserCollection,ChatResponse,MessagesResponse,MessageResponse,UserInDB
from backend.auth import get_current_user
from typing import List


chat_router = APIRouter(prefix="/chats",tags=["Chats"])

@chat_router.get("",response_model=chatCollection,description="this api call gets all the chats for a user")
def get_chats(session: Session = Depends(db.get_session),user: UserInDB = Depends(get_current_user)):
    chats=db.get_all_chats(session,user)
    return chatCollection( meta={"count":len(chats)} , chats=chats)

@chat_router.put("/{chat_id}",response_model = ChatResponse ,description="this api call changes the name of the particular chat witht the given name or if the chat does not exists then raises 404")
def create_user(chat_create: chatCreate,chat_id:int,session: Session = Depends(db.get_session)):
    return db.put_chat(session,chat_id,chat_create)


@chat_router.get("/{chat_id}/messages",response_model=MessagesResponse,description="gets the messages for the particular chat id ")
def get_chat_messages(chat_id:str,session: Session = Depends(db.get_session),user: UserInDB = Depends(get_current_user)):
    return db.get_messages(session,chat_id,user)


@chat_router.get("/{chat_id}/users",response_model=UserCollection ,description="gets all the users for the given chat id")
def get_chat_user(chat_id:str,session: Session = Depends(db.get_session),user: UserInDB = Depends(get_current_user)):
    return db.get_chat_users(session,chat_id,user)

@chat_router.post("/{chat_id}/messages",response_model =MessageResponse,status_code=201)
def putChatMessage(chat_id:str,message:messageCreate ,user: UserInDB = Depends(get_current_user),session :Session =  Depends(db.get_session)):
    return db.updateChat(session,chat_id,user,message.text)

@chat_router.get("/{chat_id}")
def getChat(chat_id:str,session :Session =  Depends(db.get_session),include: List[str] =Query(None),user: UserInDB = Depends(get_current_user)):
    return db.getChat(chat_id,session,include,user)

@chat_router.delete("/{chat_id}/messages/{message_id}", status_code=204)
def deleteUserText(chat_id:str,message_id:str , session :Session =  Depends(db.get_session),user: UserInDB = Depends(get_current_user)):
    #this method will delete the text if the current user is the owner of the
    # text
    return db.delMessage(chat_id,message_id,session,user)
    

@chat_router.put("/{chat_id}/messages/{message_id}",response_model =MessageResponse)
def updateTheUserText(chat_id:str, message_id:str , message:messageCreate,session :Session =  Depends(db.get_session),user: UserInDB = Depends(get_current_user)):
    #this method will get the user from authorisation
    #and then if the user is the owner of the text he will be able to update the text
    #and if the user is not the owner of the message there will be an error
    return db.updateUserMessage(chat_id,message_id,session,user,message)


