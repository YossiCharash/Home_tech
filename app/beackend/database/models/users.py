from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.beackend.database import Base


class Users(Base):
    __tablename__ = 'users'

    internal_id = Column(Integer, primary_key=True)
    id = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True)
    reputation_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # תקן את הקשרים
    offers = relationship("Offer", back_populates="buyer")
    system_user = relationship("SystemUsers", back_populates="real_user", uselist=False)
