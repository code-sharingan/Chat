import os
from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import SQLModel ,Session,select
from backend.entities import User,UserInDB,UserResponse
from passlib.context import CryptContext
from backend import database as db
from pydantic import BaseModel,ValidationError
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime,timezone
from jose import ExpiredSignatureError,JWTError,jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_router= APIRouter(prefix="/auth" , tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
access_token_duration = 3600 # this is in seconds
jwt_key= os.environ.get("JWT_KEY",default="insecure-jwt-key-for-dev")
jwt_algo="HS256"
class Claims(BaseModel):
    """access token claims"""
    sub:str 
    exp:int 

class UserResgistration(SQLModel):
    """request model to register new user"""
    username:str
    email:str 
    password:str

class AccessToken(BaseModel):
    """response model for access token"""
    access_token:str 
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


class InvalidToken(AuthException):
   def __init__(self):
        super().__init__(
            error="invalid_client",
            description="invlaid bearer token",
        )
class ExpiredToken(AuthException):
    def __init__(self):
        super().__init__(
            error="token_expired",
            description="expired bearer token",
        )

@auth_router.post("/registration",response_model = UserResponse,status_code=status.HTTP_201_CREATED)
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
    return UserResponse(user=user)

@auth_router.post("/token",response_model=AccessToken)
def get_access_token(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(db.get_session)):
    """Get the access token for the user"""
    user= _get_authenticated_user(session,form)
    return _build_access_token(user)



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

def _build_access_token(user: UserInDB)->AccessToken:
    expiration = int (datetime.now(timezone.utc).timestamp())+access_token_duration
    claims = Claims(sub=str(user.id) , exp= expiration)
    access_token = jwt.encode(claims.model_dump(),key=jwt_key,algorithm=jwt_algo)
    return AccessToken(
        access_token=access_token,
        token_type="Bearer",
        expires_in= access_token_duration
    )


def _decode_access_token(session: Session,token:str):
    try:
        claims = Claims(**jwt.decode(token,key=jwt_key,algorithms=[jwt_algo]))
        user_id=claims.sub
        user = session.get(UserInDB,user_id)

        if user is None:
            raise InvalidToken()
        return user
    except ExpiredSignatureError:
        raise ExpiredToken()
    except JWTError:
        raise InvalidToken()
    except ValidationError:
        raise InvalidToken()