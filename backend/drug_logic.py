import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import os

# ==================================================
# LOAD DATASET
# ==================================================

# Absolute safe path (IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "..", "datasets", "GDSC_DATASET.csv")

if not os.path.exists(DATASET_PATH):
    print("⚠️ Dataset not found:", DATASET_PATH)
    gdsc = pd.DataFrame()
else:
    try:
        gdsc = pd.read_csv(DATASET_PATH)
        print("✅ Dataset loaded successfully")
    except Exception as e:
        print("❌ Error loading dataset:", e)
        gdsc = pd.DataFrame()

# ==================================================
# PREPROCESS DATA
# ==================================================

sorted_drugs = pd.DataFrame()

if not gdsc.empty:
    try:
        y = gdsc["LN_IC50"]

        drop_cols = [
            "LN_IC50",
            "DRUG_ID",
            "DRUG_NAME",
            "COSMIC_ID",
            "CELL_LINE_NAME",
            "TCGA_DESC",
            "GDSC Tissue descriptor 1",
            "GDSC Tissue descriptor 2",
            "Cancer Type (matching TCGA label)",
            "Microsatellite instability Status (MSI)",
            "Screen Medium",
            "Growth Properties",
            "TARGET",
            "TARGET_PATHWAY"
        ]

        X = gdsc.drop(columns=drop_cols, errors="ignore")

        # Keep only numeric columns
        X = X.select_dtypes(include=["float64", "int64"])

        # Train model
        drug_model = RandomForestRegressor(
            n_estimators=20,
            random_state=42,
            n_jobs=-1
        )

        drug_model.fit(X, y)

        # Predict effectiveness
        gdsc["Predicted_LN_IC50"] = drug_model.predict(X)

        # Sort drugs
        sorted_drugs = (
            gdsc[["DRUG_NAME", "Predicted_LN_IC50"]]
            .drop_duplicates()
            .sort_values("Predicted_LN_IC50")
            .reset_index(drop=True)
        )

        print("✅ Drug model trained successfully")

    except Exception as e:
        print("❌ Error during preprocessing:", e)
        sorted_drugs = pd.DataFrame()

# ==================================================
# RISK CLASSIFICATION
# ==================================================

def get_patient_risk_category(patient):
    try:
        radius = float(patient.get("radius_mean", 0))
        area = float(patient.get("area_mean", 0))
        perimeter = float(patient.get("perimeter_mean", 0))
    except:
        return "unknown"

    if area > 1400 and perimeter > 150:
        return "high_risk"
    elif radius > 18:
        return "medium_risk"
    else:
        return "low_risk"

# ==================================================
# DRUG SELECTION
# ==================================================

def select_drug_based_on_patient(patient):

    if sorted_drugs.empty:
        return {
            "drug": "No Drug Available",
            "risk": "unknown"
        }

    category = get_patient_risk_category(patient)

    total = len(sorted_drugs)

    if total == 0:
        return {
            "drug": "No Drug Available",
            "risk": "unknown"
        }

    high_range = sorted_drugs.iloc[0:int(total * 0.3)]
    mid_range = sorted_drugs.iloc[int(total * 0.3):int(total * 0.6)]
    low_range = sorted_drugs.iloc[int(total * 0.6):]

    if category == "high_risk":
        candidates = high_range
    elif category == "medium_risk":
        candidates = mid_range
    else:
        candidates = low_range

    if candidates.empty:
        candidates = sorted_drugs

    selected_row = candidates.sample(n=1).iloc[0]

    return {
        "drug": selected_row["DRUG_NAME"],
        "risk": category
    }

# ==================================================
# MAIN FUNCTION
# ==================================================

def recommend_drug(patient):
    return select_drug_based_on_patient(patient)
