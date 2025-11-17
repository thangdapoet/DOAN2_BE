from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class History(Base):
    __tablename__ = "history"

    HistoryId = Column(Integer, primary_key=True, index=True)
    ImageUrl = Column(String)
    CreatedDate = Column(DateTime(timezone=True), server_default=func.now())
    UID = Column(String)
    Status = Column(String)
