# import sentry_sdk
from fastapi import FastAPI,APIRouter
from fastapi.routing import APIRoute
from app.api.main import app_router
from app.db import Base,engine


app = FastAPI()

api_router = APIRouter(prefix='/api')

Base.metadata.create_all(bind=engine)

api_router.include_router(app_router)

@api_router.get('/')
def read_root():
    return {"hello":'world'}

app.include_router(api_router)