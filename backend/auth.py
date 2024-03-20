from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import SQLModel ,Session,select
from backend.entities import User,UserInDB
from passlib.context import CryptContext
from backend import database as db
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime,timezone
from jose import ExpiredSignatureError,JWSError,jwt



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_router= APIRouter(prefix="/auth" , tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
acess_token_duration = 3600 # this is in seconds
jwt_key="insecure-jwt-key"
jwt_algo="HS256"
class Claims(BaseModel):
    """acess token claims"""
    subject:str 
    exp:int 

class UserResgistration(SQLModel):
    """request model to register new user"""
    username:str
    email:str 
    password:str

class AcessToken(BaseModel):
    """response model for acess token"""
    acess_token:str 
    token_type:str 
    expires_in: int

class AuthException(HTTPException):
    def __init__(self, error:str,description:str ):
        super().__init__(
            status_code=401,
            detail={
                "error":error,
                "error_description":description,
            },
        )

class InvalidCredentials(AuthException):
    def __init__(self):
        super().__init__(
            error="invlaid_client",
            description="invlaid username or password",
        )

@auth_router.post("/resgistration",response_model = User)
def register_new_user(register:UserResgistration,session: Session = Depends(db.get_session)):
    """Register a new user to the database"""
    hashed_pass = pwd_context.hash(register.password)
    user = UserInDB(
        username=register.username,
        email=register.email,
        hashed_password=hashed_pass
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@auth_router.post("/token",response_model=AcessToken)
def get_acess_token(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(db.get_session)):
    """Get the access token for the user"""
    user= _get_authenticated_user(session,form)
    return _build_acess_token(user)



def get_current_user(
        session: Session= Depends(db.get_session),
        token:str = Depends(oauth2_scheme),
)->UserInDB:
    user = _decode_access_token(session,token)
    print("this is the user --------------------------------------------------------")
    print(user)
    return user



def _get_authenticated_user(session: Session,form: OAuth2PasswordRequestForm)->UserInDB:
    user = session.exec(
        select(UserInDB).where(UserInDB.username ==  form.username)
        ).first()
    if user is None or not pwd_context.verify(form.password,user.hashed_password):
        raise InvalidCredentials()
    return user

def _build_acess_token(user: UserInDB)->AcessToken:
    expiration = int (datetime.now(timezone.utc).timestamp())+acess_token_duration
    claims = Claims(subject=str(user.id) , exp= expiration)
    access_token = jwt.encode(claims.model_dump(),key=jwt_key,algorithm=jwt_algo)
    return AcessToken(
        acess_token=access_token,
        token_type="bearer",
        expires_in= acess_token_duration
    )


def _decode_access_token(session: Session,token:str):
    claims = Claims(**jwt.decode(token,key=jwt_key,algorithms=[jwt_algo]))
    user_id=claims.subject
    return session.get(UserInDB,user_id)