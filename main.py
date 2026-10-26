from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import joblib
from typing import List

from database import engine, get_db
from models import Base, PatientRecord
from drug_logic import recommend_drug
from auth import router as auth_router
from dependencies import get_current_user
from schemas import PatientInput, PredictionResponse, PatientHistory

from fastapi.middleware.cors import CORSMiddleware


# -----------------------------------
# FASTAPI APP (ONLY ONCE)
# -----------------------------------
app = FastAPI(
    title="SMARTCARE Backend API",
    description="AI-powered breast cancer detection and drug recommendation system",
    version="1.0"
)


# -----------------------------------
# CORS (IMPORTANT FOR FRONTEND)
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# DATABASE SETUP
# -----------------------------------
Base.metadata.create_all(bind=engine)


# -----------------------------------
# ROUTERS
# -----------------------------------
app.include_router(auth_router)


# -----------------------------------
# LOAD MODEL SAFELY
# -----------------------------------
try:
    cancer_model = joblib.load("cancer_model.pkl")
    print("✅ Cancer model loaded successfully")
except Exception as e:
    print("❌ Model loading failed:", e)
    cancer_model = None


# -----------------------------------
# FEATURES
# -----------------------------------
FEATURES = [
    "radius_mean",
    "area_mean",
    "radius_worst",
    "area_worst",
    "perimeter_mean",
    "perimeter_worst"
]


# -----------------------------------
# PREDICT API
# -----------------------------------
@app.post("/predict", response_model=PredictionResponse)
def predict_patient(
    patient: PatientInput,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if cancer_model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")

        print("📥 Received patient data:", patient)

        # Convert input
        patient_df = pd.DataFrame([patient.dict()])[FEATURES]

        # Prediction
        prediction = cancer_model.predict(patient_df)[0]
        probability = cancer_model.predict_proba(patient_df)[0][1]

        status = "Healthy"
        drug_name = None
        risk_category = None

        # If cancer detected
        if prediction == 1:
            status = "Cancer Detected"

            patient_dict = {
                "radius_mean": patient.radius_mean,
                "area_mean": patient.area_mean,
                "perimeter_mean": patient.perimeter_mean
            }

            result = recommend_drug(patient_dict)

            if isinstance(result, dict):
                drug_name = result.get("drug")
                risk_category = result.get("risk")

        # Save to DB
        record = PatientRecord(
            user_id=user.id,
            radius_mean=patient.radius_mean,
            area_mean=patient.area_mean,
            radius_worst=patient.radius_worst,
            area_worst=patient.area_worst,
            perimeter_mean=patient.perimeter_mean,
            perimeter_worst=patient.perimeter_worst,
            diagnosis=status,
            confidence=round(probability * 100, 2),
            risk_category=risk_category,
            recommended_drug=drug_name
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        # Response
        if status == "Healthy":
            return {
                "status": status,
                "confidence": round((1 - probability) * 100, 2),
                "risk_category": None,
                "recommended_drug": None
            }

        return {
            "status": status,
            "confidence": round(probability * 100, 2),
            "risk_category": risk_category,
            "recommended_drug": drug_name
        }

    except Exception as e:
        print("❌ Error in prediction:", e)
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------
# PATIENT HISTORY
# -----------------------------------
@app.get("/my-patients", response_model=List[PatientHistory])
def my_patients(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        records = db.query(PatientRecord).filter(
            PatientRecord.user_id == user.id
        ).all()

        return records   # automatic conversion

    except Exception as e:
        print("❌ Error fetching history:", e)
        raise HTTPException(status_code=500, detail=str(e))
