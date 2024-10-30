from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, UniqueConstraint, Index, JSON
from sqlalchemy.orm import declarative_base

from app.models.base import Base

class TypesenseErrorResponse(Base):
    __tablename__ = 'typesenseerrorresponse'
    errorCode = Column(String, nullable=True)
    retryAttempt = Column(Integer, nullable=True)
    message = Column(String, nullable=True)
    details = Column(String, nullable=True)
    id = Column(Integer, primary_key=True, autoincrement=True)