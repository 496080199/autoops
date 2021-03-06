# -*- coding:utf-8 -*-  
from sqlalchemy import *
from sqlalchemy.orm import relationship,backref
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from db import *


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
class Class(Base):
    __tablename__='Class'
    id=Column(INTEGER, primary_key = True)
    name=Column(VARCHAR(20),nullable=False)
    prod=relationship("Prod", back_populates="classify")
class Prod(Base):
    __tablename__='Prod'
    id=Column(INTEGER, primary_key = True)
    name=Column(VARCHAR(20),nullable=False)
    env_id=Column(Integer,ForeignKey('Env.id'))
    class_id=Column(Integer,ForeignKey('Class.id'),default=1)
    classify = relationship("Class", back_populates="prod")
    conf=relationship("Conf",uselist=False, back_populates="prod")
    conffile=relationship("Conffile")
    ver=relationship("Ver")
    publog=relationship("Publog")
class Conf(Base):
    __tablename__='Conf'
    id=Column(INTEGER, primary_key = True)
    prod_id=Column(Integer,ForeignKey('Prod.id'))
    prod=relationship("Prod", back_populates="conf")
    rules=Column(TEXT(500),nullable=False,default="---\n")
    hosts=Column(TEXT(100),nullable=False,default="")
    fetch=Column(BOOLEAN,nullable=False,default=False)
    host=Column(VARCHAR(100),default="")
    src=Column(VARCHAR(100),default="")
    
class Conffile(Base):
    __tablename__='Conffile'
    id=Column(INTEGER, primary_key = True)
    name=Column(VARCHAR(20),nullable=False)
    time=Column(DATETIME,nullable=False,default=datetime.now())
    prod_id=Column(Integer,ForeignKey('Prod.id'))
    file=Column(VARCHAR(100),nullable=False)
class Ver(Base):
    __tablename__='Ver'
    id=Column(INTEGER, primary_key = True)
    name=Column(VARCHAR(20),nullable=False)
    prod_id=Column(Integer,ForeignKey('Prod.id'))
    major=Column(Integer,nullable=False)
    minor=Column(Integer,nullable=False)
    revison=Column(Integer,nullable=False)
    pub_time=Column(DATETIME,nullable=False,default=datetime.now())
    ch_time=Column(DATETIME,nullable=False,default=datetime.now())
    file=Column(VARCHAR(100),nullable=False)
    timepub=relationship("Timepub",uselist=False, back_populates="ver")
class Timepub(Base):
    __tablename__='Timepub'
    id=Column(INTEGER, primary_key = True)
    ver_id=Column(Integer,ForeignKey('Ver.id'))
    ver=relationship("Ver", back_populates="timepub")
    time=Column(BOOLEAN,nullable=False,default=False)
    min=Column(VARCHAR(10),nullable=False,default="0")
    hour=Column(VARCHAR(10),nullable=False,default="0")
    day=Column(VARCHAR(10),nullable=False,default="*")
    mon=Column(VARCHAR(10),nullable=False,default="*")
    week=Column(VARCHAR(10),nullable=False,default="*")
class Publog(Base):
    __tablename__='Publog'
    id=Column(INTEGER, primary_key = True)
    prod_id=Column(Integer,ForeignKey('Prod.id'))
    user=Column(VARCHAR(20),nullable=False)
    time=Column(DATETIME,nullable=False,default=datetime.now())
    log=Column(VARCHAR(100),nullable=False)
    content=Column(TEXT,nullable=False)
    
class Config(Base):
    __tablename__='Config'
    id=Column(INTEGER, primary_key = True)
    key=Column(VARCHAR(30),nullable=False)
    value=Column(VARCHAR(100),nullable=False)

Base.metadata.create_all(engine)