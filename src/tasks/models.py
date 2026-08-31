from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from src.utils.db import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    isCompleted = Column(Boolean, default=False)
    createdAt = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    
