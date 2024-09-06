import os
from dotenv import load_dotenv

load_dotenv()
PORT = os.getenv("PORT")
HOST= os.getenv('HOST')
DATABASE_URL = os.getenv('DATABASE_URL')
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM=os.getenv('ALGORITHM')