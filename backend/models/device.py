"""Device database model for ESP32 management"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base


class Device(Base):
    """Device model for managing ESP32 devices"""

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_name = Column(String, nullable=False)
    device_id = Column(String, unique=True, index=True, nullable=False)  # Unique ESP32 identifier
    api_key = Column(String, nullable=False)  # Device-specific API key
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Device info
    firmware_version = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="devices")

    def __repr__(self):
        return f"<Device(id={self.id}, device_name={self.device_name}, device_id={self.device_id})>"
