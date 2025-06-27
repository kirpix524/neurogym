from sqlalchemy import Column, Integer
from app.infrastructure.db import db

class BaseData(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
