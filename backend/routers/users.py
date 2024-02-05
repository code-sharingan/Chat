from fastapi import APIRouter,HTTPException
from datetime import date
from typing import Literal
from backend import database as db


from backend.entities import UserCollection,User,userCreate,userIDB,chatCollection

user_router = APIRouter(prefix="/users",tags=["users"])

@user_router.get("",response_model=UserCollection,description="this api call returns all the users in the database")
def get_users():
    sort_key=lambda user: user.id
    users = db.get_all_users()
    return UserCollection(
        meta={"count":len(users)},
        users=sorted(users,key=sort_key)
    )


@user_router.get("/{user_id}" , response_model=userIDB,description="get a user with that particular id")
def get_user(user_id:str): 
    return userIDB(user=db.get_user_by_id(user_id))


@user_router.post("",response_model = userIDB ,description="this api call adds the particular user to the database")
def create_user(user_create: userCreate):
    if(db.user_exists(user_create.id)):
        raise HTTPException(status_code =422 , detail={"detail":{"type":"duplicate_entity" , "entity_name":"User","entity_id":user_create.id}})
    return userIDB(user=db.create_user(user_create))


@user_router.get("/{user_id}/chats", response_model= chatCollection,description="this api9 call gets all the chats in which the partticular user is an active participant")
def get_user_chats(user_id:str)->chatCollection:
    sort_key = lambda Chat: Chat.name
    if(not db.user_exists(user_id)):
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"User","entity_id":user_id}})
    chats_list = db.get_user_chats(user_id)
    return chatCollection(meta={"count":len(chats_list)} , chats=sorted(chats_list,key =sort_key))