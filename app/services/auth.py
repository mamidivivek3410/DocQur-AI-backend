from sqlalchemy.orm import Session
from app.schemas import UserCreateSchema
from app.models import User
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Annotated
from config.utils import handle_controller_error
from app.db import get_db
from datetime import timedelta,datetime
from jose import jwt,JWTError
from config.globals import JWT_SECRET,ALGORITHM

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
db_dependency = Annotated[Session,Depends(get_db)]

class Auth:
    def __init__(self,db:db_dependency):
        print(db)
        self.db = db
    
    def register(self,create_user_request:UserCreateSchema):
        try:
            existing_user = self.db.query(User).filter(User.username == create_user_request.username).first()
            if existing_user:
                raise HTTPException(status_code=400,detail="User already exists")
            create_user_model = User(
                username=create_user_request.username,
                email=create_user_request.email,
                password=bcrypt_context.hash(create_user_request.password)
                )
            self.db.add(create_user_model )
            self.db.commit()
            self.db.refresh(create_user_model)
            
            return create_user_model
        except Exception as e:
            print("Error in registering:",e)
            handle_controller_error(e)
    
    def login_access_token(self,form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
        try:
            user = self.authenticate_user(form_data.username,form_data.password)
            print(user.username)
            if user is None:
                raise HTTPException(status_code=400,detail="Invalid credentials")
            token = self.create_access_token(user.username,user.id,timedelta(minutes=20))
            
            return {'access_token':token,'token_type':'bearer'}
        except Exception as e:
            raise HTTPException(status_code=500,detail=e)

    def authenticate_user(self,username:str,password:str):
        try:
            user = self.db.query(User).filter(User.username==username).first()
            # print(bcrypt_context.verify(password,user.password))
            if not user:
                return False
            if not bcrypt_context.verify(password,user.password):
                return False
            return user
        except Exception as e:
            raise HTTPException(status_code=401,detail="not Generate")
    
    def create_access_token(self,username:str,user_id:int,expires_delta:timedelta):
        encode = {'sub':username,'id':user_id}
        expires = datetime.utcnow() + expires_delta
        encode.update({'exp':expires})
        return jwt.encode(encode,JWT_SECRET,algorithm=ALGORITHM)
        
    def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(token,JWT_SECRET,algorithms=[ALGORITHM])
            username: str = payload.get('sub')
            user_id: int = payload.get('id')
            if username is None or user_id is None:
                raise HTTPException(status_code=401,detail='Could not validate user')
            return {'username':username,'id':user_id}
        except JWTError:
            raise HTTPException(status_code=401,detail="Could not validate user")