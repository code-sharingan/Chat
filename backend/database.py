import json
from datetime import date ,datetime
from uuid import uuid4
from fastapi import HTTPException
from sqlmodel import Session, SQLModel, create_engine, select
from backend.entities import User,userCreate,Chat,chatCreate, UserInDB ,ChatInDB
with open("backend/fake_db.json","r") as f:
    Db = json.load(f)



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


def user_exists(id:str):
    if id in Db["users"]:
        return True
    return False


def get_user_chats(session :Session ,user_id:str)->list[Chat]:
    chats=[]
    query =(select(ChatInDB).join(ChatInDB.users).filter(UserInDB.id == user_id))
    chats = session.exec(query).all()
    # for id,chat_data in Db["chats"].items():
    #     if(user_id in chat_data["user_ids"]):
    #         chat =Chat(**chat_data)
    #         chats.append(chat)
    print("-------------------chats------------------")
    print(chats)
    return chats
            

# ------------------------------chats---------------------------------------------

def get_all_chats():
    return [Chat(**chat_data) for chat_data in Db["chats"].values()]

def get_chat(chat_id:str):
    if(chat_id in Db["chats"]):
        return Chat(**Db["chats"][chat_id])
    else:
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})

def put_chat(chat_id:str ,chat_create:chatCreate):
    if(chat_id not in Db["chats"]):
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})
    else:
        Db["chats"][chat_id]["name"] = chat_create.name
    return Chat(**Db["chats"][chat_id])

def del_chat(chat_id):
    chat=get_chat(chat_id)
    del Db["chats"][chat_id]


def get_messages(chat_id:str):
    if(chat_id not in Db["chats"]):
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})
    chat_data = Db["chats"][chat_id]
    return chat_data.get("messages",[])

def get_chat_user(chat_id:str):
    if(chat_id not in Db["chats"]):
        raise HTTPException(status_code =404 , detail={"detail":{"type":"entity_not_found" , "entity_name":"Chat","entity_id":chat_id}})
    chat_data=Db["chats"][chat_id]
    user_ids = chat_data.get("user_ids",[])
    user =[]
    for u in user_ids:
        user.append(get_user_by_id(u))
    return user
    

    