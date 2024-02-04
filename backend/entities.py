from datetime import date,datetime
from pydantic import BaseModel, Field

class Metadata(BaseModel):
    count:int
class User(BaseModel):
    """represents an api responsoe for a user"""
    id: str
    created_at: datetime

class UserCollection(BaseModel):
    """represents an api response for a collection of users."""
    meta: Metadata
    users: list[User]

class userIDB(BaseModel):
    user:User
class Chat(BaseModel):
    """represents an api response for a chat will be returned by GET/chats/{chat_id}"""
    id:str
    name:str
    user_ids:list[str]
    owner_id:str
    created_at:datetime

class chatCollection(BaseModel):
    """represents an api response for chats will be returned by Get/chats"""
    meta:Metadata
    chats: list[Chat]


class userCreate(BaseModel):
    id:str

class chatIDB(BaseModel):
    chat: Chat

class chatCreate(BaseModel):
    name:str

class Message(BaseModel):
    id:str
    user_id:str
    text:str
    created_at:datetime

class messagesIDB(BaseModel):
    meta:Metadata
    messages:list[Message]

