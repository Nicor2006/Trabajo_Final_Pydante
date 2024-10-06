from sqlalchemy import Column, Integer, String, DateTime
from .databases import Base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Modelo de SQLAlchemy
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    time_register = Column(DateTime, default=datetime.utcnow)
    description: Optional[str] = Column(String)
    Profesion: Optional[str] = Column(String)

# Esquema Pydantic para crear un usuario
class UserCreate(BaseModel):
    id: int
    name: str
    time_register: Optional[datetime] = None
    description: Optional[str] = Column(String)
    Profesion: Optional[str] = Column(String)

# Esquema Pydantic para la respuesta de usuario
class User(BaseModel):
    id: int
    name: str
    time_register: Optional[datetime] = None
    description: Optional[str] = Column(String)
    Profesion: Optional[str] = Column(String)


    class Config:
        orm_mode = True