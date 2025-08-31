from datetime import datetime

from app.beackend.database import Base
from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship


# 3. מודל הצעות מחיר (Offers)
class Offer(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties_details.id'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.internal_id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum('pending', 'accepted', 'rejected', 'withdrawn', name='offer_status_enum'), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # יחסים
    property = relationship("PropertyDetails", back_populates="offers")
    buyer = relationship("Users", back_populates="offers")