from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Enum, String, ForeignKey
from sqlalchemy.orm import relationship

from app.beackend.database import Base


class SystemUsers(Base):
    __tablename__ = 'system_users'

    id = Column(Integer, primary_key=True)
    system_username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum('admin', 'moderator', name='user_role_enum'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.internal_id"))  # קישור למשתמש בטבלת Users, אם יש צורך

    real_user = relationship("Users", back_populates="system_user")
    properties = relationship("PropertyDetails", back_populates="system_user")
    offers = relationship("Offer", back_populates="system_user")