import os
import sys ,datetime
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String(250),nullable=False)
    user_type = Column(String(250), nullable=False)
    password = Column(String(250))
    
class Patients(Base):
    __tablename__='patients'
    ssn_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250),nullable=False)
    age = Column(Integer,nullable=False)
    DateofAdm =  Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    TypeofBed = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)