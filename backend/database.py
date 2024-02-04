import json
from datetime import date
from uuid import uuid4
from fastapi import HTTPException

from backend.entities import User,userCreate,Chat
with open("backend/fake_db.json","r") as f:
    Db = json.load(f)

class EntityNotFoundException(Exception):
    def __init__(self,*,entity_name:str,entity_id:str):
        self.entity_name =entity_name
        self.entity_id=entity_id


#--------------------users-------------------------------
        

def get_all_users()->list[User]:
    """retreive list of all the users in the db
        returns ordered list of all the users"""
    
    return [User(**user_data) for user_data in Db["users"].values()]

def get_user_by_id(user_id:str)->User:
    """retreives the user form the database with the given user id"""
    if user_id in Db["users"]:
        return User(**Db["users"][user_id])
    raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"User","entity_id":user_id}})


def create_user(user_create :userCreate) ->User:
    """this is the backend method that puts in a new user to the database"""
    user= User(created_at=date.today(), 
               **user_create.model_dump(),)
    Db["users"][user.id] = user.model_dump()
    return user


def user_exists(id:str):
    if id in Db["users"]:
        return True
    return False


def get_user_chats(user_id:str)->list[Chat]:
    chats=[]
    for id,chat_data in Db["chats"].items():
        if(user_id in chat_data["user_ids"]):
            chat =Chat(**chat_data)
            chats.append(chat)
    return chats
            

# ------------------------------chats---------------------------------------------

def get_all_chats():
    return [Chat(**chat_data) for chat_data in Db["chats"].values()]