from fastapi import APIRouter
from datetime import date
from typing import Literal
import backend.database as db

from backend.entities import UserCollection

user_router = APIRouter(prefix="/users",tags=["users"])

@user_router.get("",response_model=UserCollection)
def get_users():
    sort_key=lambda user: getattr(user,user.id)
    users = db.get_all_users()
    return UserCollection(
        meta={"count":len(users)},
        users=sorted(users,key=sort_key)
    )