from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str