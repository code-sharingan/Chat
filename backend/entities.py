from datetime import date,datetime
from pydantic import BaseModel, Field
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional

class Metadata(BaseModel):
    count:int
class Metadata2(BaseModel):
    message_count:int
    user_count:int
class User(SQLModel):
    """represents an api responsoe for a user"""
    id: int
    username: str
    email:str
    created_at: datetime
class UserResponse(SQLModel):
    user:User
class UserCollection(BaseModel):
    """represents an api response for a collection of users."""
    meta: Metadata
    users: list[User]

class UserChatLinkInDB(SQLModel, table=True):
    """Database model for many-to-many relation of users to chats."""

    __tablename__ = "user_chat_links"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    chat_id: int = Field(foreign_key="chats.id", primary_key=True)


class UserInDB(SQLModel, table=True):
    """Database model for user."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    chats: list["ChatInDB"] = Relationship(
        back_populates="users",
        link_model=UserChatLinkInDB,
    )

class userCreate(SQLModel):
    username:str
    email:str
    hashed_password:str


class userUpdate(SQLModel):
    username:Optional[str]=None
    email:Optional[str]=None



# --------------------------------------chats model------------------------------------------------------
class Chat(SQLModel):
    """represents an api response for a chat will be returned by GET/chats/{chat_id}"""
    id:int
    name:str
    owner:User
    created_at:datetime
class ChatResponse(SQLModel):
    chat:Chat
class userChat(SQLModel):
    meta:Metadata
    chats: list[Chat]
class chatCollection(SQLModel):
    """represents an api response for chats will be returned by Get/chats"""
    meta:Metadata
    chats: list[Chat]

class chatCreate(BaseModel):
    name:str


class ChatInDB(SQLModel, table=True):
    """Database model for chat."""

    __tablename__ = "chats"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner: UserInDB = Relationship()
    users: list[UserInDB] = Relationship(
        back_populates="chats",
        link_model=UserChatLinkInDB,
    )
    messages: list["MessageInDB"] = Relationship(back_populates="chat")




class Message(SQLModel):
    id:int
    text:str
    chat_id:int
    user:User
    created_at:datetime

class newChatResponse1(SQLModel):
    meta:Metadata2
    chat:Chat
class newChatResponse2(SQLModel):
    meta:Metadata2
    chat:Chat
    users:Optional[list[User]]
class newChatResponse3(SQLModel):
    meta:Metadata2
    chat:Chat
    messages:Optional[list[Message]]
class newChatResponse4(SQLModel):
    meta:Metadata2
    chat:Chat
    messages:Optional[list[Message]]
    users:Optional[list[User]]

class MessagesResponse(SQLModel):
    meta: Metadata
    messages: list[Message]

class MessageResponse(SQLModel):
    message: Message
class MessageInDB(SQLModel, table=True):
    """Database model for message."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    user_id: int = Field(foreign_key="users.id")
    chat_id: int = Field(foreign_key="chats.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: UserInDB = Relationship()
    chat: ChatInDB = Relationship(back_populates="messages")

class chatMessageText(SQLModel):
    text: str
