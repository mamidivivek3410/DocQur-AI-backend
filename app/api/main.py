from fastapi import APIRouter
from app.api.app.auth import auth_router
app_router = APIRouter(prefix='/app')

@app_router.get('/health-check')
def health_check():
    return "OK"

app_router.include_router(auth_router,tags=['auth'])
