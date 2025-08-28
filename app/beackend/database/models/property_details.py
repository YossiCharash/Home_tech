from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship

from app.beackend.database import Base


class PropertyDetails(Base):
    __tablename__ = 'properties_details'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('users.internal_id'), nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    zipcode = Column(String, nullable=True)
    area_sqm = Column(Integer, nullable=True)
    rooms = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    listing_type = Column(Enum('hybrid', 'auction', name="listing_type_enum"), nullable=False)
    price = Column(DECIMAL(10, 2))  # דיוק של 10 ספרות, 2 אחרי הנקודה
    status = Column(Enum('active', 'pending_sale', 'sold', 'canceled', name='property_status_enum'), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    seller = relationship("Users", back_populates="properties")
    offers = relationship("Offer", back_populates="property")
    system_user = relationship("SystemUsers", back_populates="properties")