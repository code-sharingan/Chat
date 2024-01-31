import json
from datetime import date
from uuid import uuid4

from backend.entities import User

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