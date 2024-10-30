from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, UniqueConstraint, Index, JSON
from sqlalchemy.orm import declarative_base

from app.models.base import Base

class SuccessResponse(Base):
    __tablename__ = 'successresponse'
    message = Column(String, nullable=True)
    id = Column(Integer, primary_key=True, autoincrement=True)