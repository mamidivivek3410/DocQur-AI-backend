from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    username = Column(String,index=True)
    email=Column(String,unique=True,index=True)
    password = Column(String)
    
# class Document(Base):
#     __tablename__ = 'documents'
    
#     id = Column(integer,primary_key=True,index=True)
#     title = Column(String)
#     s3_url = Column(String)
#     uploaded_at = Column(DateTime,default=datetime.utcnow)
#     user_id = relationship('User',back_populates='documents')