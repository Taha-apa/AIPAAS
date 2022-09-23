
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship,declarative_base
from flask_login import UserMixin
from . import db
class User(UserMixin,db.Model) :
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(100),unique = True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    codes = relationship("CodeData")    
    dataSets = relationship("DataSet")
class CodeData(UserMixin,db.Model):
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey("user.id"))
    codeName = Column(String(100))
    code = Column(Text)
class DataSet(UserMixin,db.Model):
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey("user.id"))
    codeName = Column(String(100))
    code = Column(Text)