from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


# -----------------------------------------
# USER TABLE
# -----------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Relationship with patient records
    patients = relationship(
        "PatientRecord",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select"
    )

    def __repr__(self):
        return f"<User(username={self.username})>"


# -----------------------------------------
# PATIENT RECORD TABLE
# -----------------------------------------
class PatientRecord(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key (User)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # -------------------------------
    # INPUT FEATURES
    # -------------------------------
    radius_mean = Column(Float, nullable=False)
    area_mean = Column(Float, nullable=False)
    radius_worst = Column(Float, nullable=False)
    area_worst = Column(Float, nullable=False)
    perimeter_mean = Column(Float, nullable=False)
    perimeter_worst = Column(Float, nullable=False)

    # -------------------------------
    # PREDICTION OUTPUT
    # -------------------------------
    diagnosis = Column(String(50), nullable=False)   # Healthy / Cancer

    confidence = Column(Float, nullable=False)       # Always stored
    risk_category = Column(String(50), nullable=True)
    recommended_drug = Column(String(100), nullable=True)

    # -------------------------------
    # TIMESTAMP
    # -------------------------------
    created_at = Column(DateTime, default=datetime.utcnow)

    # -------------------------------
    # RELATIONSHIP
    # -------------------------------
    user = relationship("User", back_populates="patients")

    def __repr__(self):
        return f"<PatientRecord(id={self.id}, diagnosis={self.diagnosis})>"
