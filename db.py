# -*- coding:utf-8 -*- 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root@localhost/test?charset=utf8', echo=False)
DB_Session = sessionmaker(bind=engine)