from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -----------------------------------------
# USER SCHEMAS
# -----------------------------------------

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -----------------------------------------
# PATIENT INPUT SCHEMA
# -----------------------------------------

class PatientInput(BaseModel):
    radius_mean: float = Field(..., gt=0)
    area_mean: float = Field(..., gt=0)
    radius_worst: float = Field(..., gt=0)
    area_worst: float = Field(..., gt=0)
    perimeter_mean: float = Field(..., gt=0)
    perimeter_worst: float = Field(..., gt=0)


# -----------------------------------------
# PREDICTION RESPONSE SCHEMA
# -----------------------------------------

class PredictionResponse(BaseModel):
    status: str
    confidence: Optional[float] = None
    risk_category: Optional[str] = None
    recommended_drug: Optional[str] = None


# -----------------------------------------
# PATIENT HISTORY RESPONSE
# -----------------------------------------

class PatientHistory(BaseModel):
    id: int
    user_id: int

    # Input
    radius_mean: float
    area_mean: float
    radius_worst: float
    area_worst: float
    perimeter_mean: float
    perimeter_worst: float

    # Output
    diagnosis: str
    confidence: Optional[float] = None
    risk_category: Optional[str] = None
    recommended_drug: Optional[str] = None

    # Timestamp
    created_at: datetime

    class Config:
        from_attributes = True   # ✅ for SQLAlchemy models
