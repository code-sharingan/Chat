import json
from datetime import date ,datetime
from uuid import uuid4
from fastapi import HTTPException
from sqlmodel import Session, SQLModel, create_engine, select
from backend.entities import User,userCreate,Chat,chatCreate, UserInDB ,ChatInDB,UserChatLinkInDB,messageCreate,ChatResponse,MessageInDB,Message,MessageInDB,MessagesResponse,UserCollection,MessageResponse,newChatResponse1,newChatResponse2,newChatResponse3,newChatResponse4
# with open("backend/fake_db.json","r") as f:
#     Db = json.load(f)
from typing import List


engine = create_engine(
    "sqlite:///backend/pony_express.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

class EntityNotFoundException(Exception):
    def __init__(self,*,entity_name:str,entity_id:str):
        self.entity_name =entity_name
        self.entity_id=entity_id


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
#--------------------users-------------------------------
        

def get_all_users(session: Session)->list[User]:
    """retreive list of all the users in the db
        returns ordered list of all the users"""
    return session.exec(select(UserInDB)).all()
    # return [User(**user_data) for user_data in Db["users"].values()]

def get_user_by_id(session: Session ,user_id:int)->User:
    """retreives the user form the database with the given user id"""
    user = session.get(UserInDB, user_id)
    if user:
        u =User(id=user.id ,username=user.username,email=user.email,created_at=user.created_at)
        return u
    raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"User","entity_id":user_id}})
    # if user_id in Db["users"]:
    #     return User(**Db["users"][user_id])
   


def create_user(session: Session, user_create :userCreate) ->User:
    """this is the backend method that puts in a new user to the database"""
    user= UserInDB(**user_create.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    # user= User(created_at=datetime.now(), 
    #            **user_create.model_dump(),)
    # Db["users"][user.id] = user.model_dump()
    # return user




def get_user_chats(session :Session ,user_id:str)->list[Chat]:
    chats = session.exec(select(ChatInDB)).all()
    chatlist=[]
    for chat in chats:
        if chat.owner_id == user_id:
            c =Chat(id = chat.id , name=chat.name,owner=chat.owner,created_at=chat.created_at )
            chatlist.append(c)
        else:
            for user in chat.users:
                if user.id == user_id:
                    c =Chat(id = chat.id , name=chat.name,owner=chat.owner,created_at=chat.created_at )
                    chatlist.append(c)
                    break

    return chatlist
            
def update_u(session:Session ,useridb:UserInDB)->User:
    session.add(useridb)
    session.commit()
    session.refresh(useridb)
    user =  User(id=useridb.id ,username=useridb.username,email=useridb.email,created_at=useridb.created_at)
    return user
    
# ------------------------------chats---------------------------------------------

def get_all_chats(session: Session,user):
    chats = session.exec(select(ChatInDB).filter(ChatInDB.users.any(UserInDB.id == user.id))).all()
    return chats


def put_chat(session:Session ,chat_id:int ,chat_create:chatCreate):
    name= chat_create.name
    chat = session.get(ChatInDB,chat_id)
    if(chat):
        chat.name= name
        session.commit()
        session.refresh(chat)
        chat_response=Chat(id=chat.id , name=chat.name,owner=chat.owner,created_at=chat.created_at)
        return ChatResponse(chat=chat_response)
    raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})

def get_messages(session: Session,chat_id:str,user):
    chat = session.get(ChatInDB,chat_id)
    if not chat:
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})
    if userChatLink(session,user.id,chat_id):
        messages = session.exec(select(MessageInDB).filter(MessageInDB.chat_id==chat_id)).all()
        if(messages):
            message_list=[]
            for m in messages:
                message = Message(id=m.id ,text=m.text,chat_id=m.chat_id,user=m.user,created_at=m.created_at)
                message_list.append(message)
            return MessagesResponse(meta={"count":len(message_list)},messages=message_list)
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})
    else:
        raise HTTPException(status_code =403 , detail={"detail":{"error":"no_permission","error_description":"requires permission to view chat"}})

    
def get_chat_users(session:Session,chat_id:int,user):
    chat = session.get(ChatInDB,chat_id)
    if not chat:
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})
    if userChatLink(session,user.id,chat_id):
        users=[]
        if(chat):
            users = chat.users # list[UserInDB], but fastapi/sqlmodel can automatically convert to list[User]
            # for u in chat.users:
            #     user= User(id=u.id ,username=u.username,email=u.email,created_at=u.created_at)
            #     users.append(user)
            return UserCollection(
                meta={"count":len(users)},
                users=users
            )
    raise HTTPException(status_code =403 , detail={"detail":{"error":"no_permission","error_description":"requires permission to view chat"}})

def updateChat(session:Session,chat_id:int,user:UserInDB,text:str):
    chat = session.get(ChatInDB,chat_id)
    if not chat:
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})
    if userChatLink(session,user.id,chat_id):    
        message =  MessageInDB(user_id=user.id,text=text,chat_id=chat_id,chat = chat,user=user)
        chat.messages.append(message)
        session.commit()
        session.refresh(chat)
        u = User(id= user.id, username =  user.username , email=user.email,created_at=user.created_at)
        m = Message(id=message.id , text =  message.text , chat_id = chat_id, user=u , created_at=message.created_at)
        return MessageResponse(message=m)           
    else:
        raise HTTPException(status_code =403 , detail={"detail":{"error":"no_permission","error_description":"requires permission to view chat"}})
def userChatLink(session,userid,chatid):
    link = session.exec(select(UserChatLinkInDB).filter_by(user_id = userid,chat_id=chatid)).first()
    return bool(link)

def getChat(chat_id , session:Session , include:List[str],user):
    chatdb = session.get(ChatInDB,chat_id)
    if not chatdb:
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})
    if userChatLink(session,user.id,chat_id):
        users = chatdb.users
        messages = chatdb.messages
        chat  = Chat(id=chatdb.id , name =  chatdb.name , owner = chatdb.owner, created_at= chatdb.created_at)
        response = newChatResponse1(meta={"message_count":len(messages) , "user_count":len(users)} , chat=chat)
        if include is not None:
            if "users" in include and "messages" in include:
                message_list=[]
                for m in messages:
                    message = Message(id=m.id ,text=m.text,chat_id=m.chat_id,user=m.user,created_at=m.created_at)
                    message_list.append(message)
                response = newChatResponse3(meta={"message_count":len(messages) , "user_count":len(users)} , chat=chat,messages=message_list)
                users=[]
                for u in chatdb.users:
                    user= User(id=u.id ,username=u.username,email=u.email,created_at=u.created_at)
                    users.append(user)
                sort_key=lambda user: user.id
                users =sorted(users,key=sort_key)
                response = newChatResponse4(meta={"message_count":len(messages) , "user_count":len(users)} , chat=chat,users=users,messages=message_list)
                return response
            if "messages" in include and "users" not in include:
                message_list=[]
                for m in messages:
                    message = Message(id=m.id ,text=m.text,chat_id=m.chat_id,user=m.user,created_at=m.created_at)
                    message_list.append(message)
                response = newChatResponse3(meta={"message_count":len(messages) , "user_count":len(users)} , chat=chat,messages=message_list)
                return response
            elif "users" in include and "messages" not in include:
                users=[]
                for u in chatdb.users:
                    user= User(id=u.id ,username=u.username,email=u.email,created_at=u.created_at)
                    users.append(user)
                sort_key=lambda user: user.id
                users =sorted(users,key=sort_key)
                response = newChatResponse2(meta={"message_count":len(messages) , "user_count":len(users)} , chat=chat,users=users)
                return response
        

        return response
    else:
        raise HTTPException(status_code =403 , detail={"detail":{"error":"no_permission","error_description":"requires permission to view chat"}})


def delMessage(chat_id,message_id,session,user):
    chatdb = session.get(ChatInDB,chat_id)
    if not chatdb:
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})
    message = session.get(MessageInDB,message_id)
    if not message:
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"message","entity_id":message_id}})
    message_user = message.user
    if(message_user.id != user.id):
        raise HTTPException(status_code =403 , detail={"detail":{"error":"no_permission","error_description":"requires permission to delete message"}})
    session.delete(message)
    session.commit()
    return None

def updateUserMessage(chat_id,message_id,session,user,m:messageCreate):
    chatdb = session.get(ChatInDB,chat_id)
    if not chatdb:
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})
    message = session.get(MessageInDB,message_id)
    if not message:
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"message","entity_id":message_id}})
    message_user = message.user
    if(message_user.id != user.id):
        raise HTTPException(status_code =403 , detail={"detail":{"error":"no_permission","error_description":"requires permission to delete message"}})
    message.text = m.text
    session.commit()
    session.refresh(message)
    return MessageResponse(message=message)
    

    