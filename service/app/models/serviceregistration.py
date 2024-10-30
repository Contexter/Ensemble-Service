from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, UniqueConstraint, Index, JSON
from sqlalchemy.orm import declarative_base

from app.models.base import Base

class ServiceRegistration(Base):
    __tablename__ = 'serviceregistration'
    id = Column(String, nullable=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    openapi_url = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)
    id = Column(Integer, primary_key=True, autoincrement=True)