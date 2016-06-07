from sqlalchemy import *
from sqlalchemy.orm import relationship,backref
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root@localhost/test', echo=False)
Base = declarative_base()

class Categories(Base):
    __tablename__='Categories'
    name=Column(VARCHAR(20),primary_key=True)
    artnum=Column(INTEGER,default=0)
    date=Column(DATETIME,default=datetime.now())
    file=Column(TEXT)
class User(Base):
    __tablename__='User'
    uid=Column(INTEGER, primary_key = True)
    username=Column(VARCHAR(20),nullable=False)
    password=Column(VARCHAR(50),nullable=False)
    
Base.metadata.create_all(engine)