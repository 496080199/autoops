# -*- coding:utf-8 -*-  
from sqlalchemy import *
from sqlalchemy.orm import relationship,backref,sessionmaker
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root@localhost/test?charset=utf8', echo=False)
DB_Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__='User'
    uid=Column(INTEGER, primary_key = True)
    username=Column(VARCHAR(20),nullable=False)
    password=Column(VARCHAR(50),nullable=False)
class Env(Base):
    __tablename__='Env'
    id=Column(INTEGER, primary_key = True)
    name=Column(VARCHAR(20),nullable=False)
    prod=relationship("Prod")
class Prod(Base):
    __tablename__='Prod'
    id=Column(INTEGER, primary_key = True)
    name=Column(VARCHAR(20),nullable=False)
    env_id=Column(Integer,ForeignKey('Env.id'))
    conf=relationship("Conf",uselist=False, back_populates="prod")
    ver=relationship("Ver")
class Conf(Base):
    __tablename__='Conf'
    id=Column(INTEGER, primary_key = True)
    name=Column(VARCHAR(20),nullable=False)
    prod_id=Column(Integer,ForeignKey('Prod.id'))
    prod=relationship("Prod", back_populates="conf")
    rules=Column(VARCHAR(100),nullable=False)
    hosts=Column(VARCHAR(100),nullable=False)
    time=Column(BOOLEAN,nullable=False)
    min=Column(VARCHAR(10),nullable=False,default="0")
    hour=Column(VARCHAR(10),nullable=False,default="0")
    day=Column(VARCHAR(10),nullable=False,default="*")
    mon=Column(VARCHAR(10),nullable=False,default="*")
    week=Column(VARCHAR(10),nullable=False,default="*")
    
class Ver(Base):
    __tablename__='Ver'
    id=Column(INTEGER, primary_key = True)
    name=Column(VARCHAR(20),nullable=False)
    prod_id=Column(Integer,ForeignKey('Prod.id'))
    major=Column(Integer,nullable=False)
    minor=Column(Integer,nullable=False)
    revison=Column(Integer,nullable=False)
    file=Column(VARCHAR(10),nullable=False)
class Config(Base):
    __tablename__='Config'
    id=Column(INTEGER, primary_key = True)
    key=Column(VARCHAR(30),nullable=False)
    value=Column(VARCHAR(100),nullable=False)

Base.metadata.create_all(engine)