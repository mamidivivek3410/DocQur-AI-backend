import fastapi
from app.schemas import UserCreateSchema
from sqlalchemy.orm import Session
from app.services.auth import Auth
from config.utils import create_error, create_response
from app.db import get_db
from passlib.context import CryptContext
from fastapi import HTTPException,APIRouter,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated

auth_router = APIRouter(prefix='/auth', tags=['auth'])

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(Auth.get_current_user)]

@auth_router.get('/health-check')
def health_check():
    return 'OK'


@auth_router.post('/register')
def register(db:db_dependency,create_user_request:UserCreateSchema):
    try:
        auth = Auth(db)
        res = auth.register(create_user_request)
        print(res)
        if res is None:
            return create_error(400,'Registration failed')
        else:
            return create_response(201,'Registered Successfully',res)
    except Exception as e:
        return create_error(500,e)


@auth_router.post('/login')
def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db: db_dependency):
    try:
        auth = Auth(db)
        res = auth.login_access_token(form_data=form_data)
        return {'status':201,'message':'Logged in successfully','data':res}
    except Exception as e:
        return {'error':e}

@auth_router.get('/')
def get_current_user(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication failed")
    return {"user:",user}