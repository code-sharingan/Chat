from fastapi import APIRouter,HTTPException,Depends
from datetime import date
from sqlmodel import Session
from backend import database as db
from backend.auth import get_current_user

from backend.entities import UserCollection,User,userCreate,UserInDB,UserResponse,userChat,Chat,Metadata

user_router = APIRouter(prefix="/users",tags=["Users"])

@user_router.get("",response_model=UserCollection,description="this api call returns all the users in the database")
def get_users(session: Session = Depends(db.get_session)):
    sort_key=lambda user: user.id
    users = db.get_all_users(session)
    return UserCollection(
        meta={"count":len(users)},
        users=sorted(users,key=sort_key)
    )

@user_router.get("/me" , response_model=UserResponse)
def get_Self(user: UserInDB = Depends(get_current_user)):
    """gte current user"""
    u = User(id=user.id ,username=user.username,email=user.email,created_at=user.created_at)
    return UserResponse(user = u)



@user_router.get("/{user_id}" , response_model=UserResponse,description="get a user with that particular id")
def get_user(user_id: int ,session: Session = Depends(db.get_session) ): 
    user = db.get_user_by_id(session,user_id)
    return UserResponse(user=user)


@user_router.post("",response_model = UserInDB ,description="this api call adds the particular user to the database")
def create_user(user_create: userCreate,session: Session = Depends(db.get_session)):
    return UserInDB(user=db.create_user(session ,user_create))


@user_router.get("/{user_id}/chats", response_model= userChat,description="this api9 call gets all the chats in which the partticular user is an active participant")
def get_user_chats(user_id:int ,session: Session = Depends(db.get_session))->userChat:
    chats_list = db.get_user_chats(session,user_id)
    chats=[]
    for chatDb in chats_list:
        chat =Chat(id = chatDb.id ,name=chatDb.name,owner=chatDb.owner,created_at=chatDb.created_at )
        chats.append(chat)
    return userChat(metadata= Metadata(count=len(chats)), chats=chats)


