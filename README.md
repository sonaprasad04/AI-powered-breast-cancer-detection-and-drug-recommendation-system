SMARTCARE: AI-Powered Breast Cancer Diagnosis and Drug Recommendation System

1. Project Overview

SMARTCARE is an academic web-application prototype that combines a breast-cancer classification model with a prototype drug-selection component. It includes user registration and login, prediction requests, and storage of prediction history in an SQLite database.

The application accepts six numerical tumour measurements and uses a saved classification model to return a prediction. If the model predicts cancer, the backend invokes the drug recommendation component.

Medical disclaimer: SMARTCARE is an educational and research prototype. Its predictions, confidence values, risk categories, and drug selections have not been established as clinically valid. Do not use this application to diagnose cancer or make treatment decisions.

2. Objectives

Explore machine-learning methods for breast-cancer classification.

Demonstrate a web API for submitting numerical tumour measurements.

Explore a prototype drug-selection workflow using drug-response data.

Provide user registration and token-based authentication.

Store prediction records and allow authenticated users to view their own history.

3. Features

User registration and login.

Password hashing and JWT-based authentication.

Breast-cancer classification using a saved model.

Drug-selection component invoked when cancer is predicted.

SQLite storage of prediction inputs and results.

Authenticated prediction-history endpoint.

HTML pages for registration, login, input, and detection.

4. Technologies

Python

FastAPI and Uvicorn

scikit-learn

Pandas and NumPy

Joblib

SQLAlchemy and SQLite

Pydantic

Passlib with bcrypt

python-jose for JWT handling

HTML

5. Machine-Learning Components

5.1 Breast-cancer classification

The backend loads backend/cancer_model.pkl. It passes these six features to the model:

radius_mean

area_mean

radius_worst

area_worst

perimeter_mean

perimeter_worst

The current backend interprets model output 1 as Cancer Detected and other output as Healthy. It uses predict_proba to calculate a percentage. The meaning of the model's class labels and the reported confidence should be confirmed against the model-training notebook before relying on them.

5.2 Drug recommendation

The current backend/drug_logic.py implementation:

Loads datasets/GDSC_DATASET.csv.

Uses LN_IC50 as the target.

Trains a RandomForestRegressor on selected numeric columns.

Predicts values for rows from the same dataset used for training.

Sorts drug records by the predicted values.

Assigns a risk category using fixed thresholds on radius_mean, area_mean, and perimeter_mean.

Randomly selects a drug from a group associated with that category.

This is a simplified prototype workflow. It does not use an individual patient's gene-expression profile to establish drug sensitivity, and it does not establish that a selected drug is suitable or effective for a patient. The risk thresholds and recommendation method have not been described as clinically validated.

6. Datasets

datasets/breast_cancer.csv

This file contains a diagnosis column and numerical tumour measurements in the familiar Wisconsin Breast Cancer Dataset format. The API code shown loads the saved model for inference; it does not read this CSV during each prediction request.

datasets/GDSC_DATASET.csv

This dataset contains drug-response fields including DRUG_NAME, LN_IC50, AUC, cell-line details, cancer-type metadata, and target/pathway metadata. The current recommendation module uses it to train its regression model at import time.

datasets/Compounds-annotation.csv

This file is present in the project. Its role in the current application has not been verified.

7. Project Structure

The following is based on the visible project files; there may be additional files in collapsed folders.

SMARTCARE/
├── backend/
│   ├── auth.py
│   ├── cancer_model.pkl
│   ├── database.py
│   ├── dependencies.py
│   ├── drug_logic.py
│   ├── jwt_token.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── smartcare.db
│
├── datasets/
│   ├── breast_cancer.csv
│   ├── Compounds-annotation.csv
│   └── GDSC_DATASET.csv
│
├── frontend/
│   ├── detection.html
│   ├── input.html
│   ├── login.html
│   └── register.html
│
├── cancer_classification.ipynb
├── drug_response_prediction.ipynb
├── final_integration.ipynb
├── pca.ipynb
├── cancer_model.pkl
├── drug_model.pkl
└── README.md

8. Setup and Installation

Prerequisites

Python installed on your system.

pip, the Python package installer.

The project files and datasets listed above.

Step 1: Open a terminal at the project root

cd SMARTCARE

Use the path to your own SMARTCARE folder if it is located elsewhere.

Step 2: Create and activate a virtual environment (recommended)

python -m venv venv

On Windows:

venv\Scripts\activate

Step 3: Create requirements.txt

Create a file named requirements.txt in the project root with this initial dependency list:

fastapi
uvicorn[standard]
sqlalchemy
pandas
numpy
scikit-learn
joblib
pydantic
python-multipart
passlib[bcrypt]
python-jose[cryptography]

Install the packages:

python -m pip install -r requirements.txt

This is an initial dependency list based on the code shared so far. If startup reports a missing module, add the package that provides it. For reproducible deployment, test the application and then pin the working package versions.

Step 4: Check required files

Verify that these paths exist:

backend/main.py

backend/cancer_model.pkl

backend/schemas.py

datasets/GDSC_DATASET.csv

The root-level cancer_model.pkl and drug_model.pkl are visible in the project, but the shown main.py specifically attempts to load cancer_model.pkl relative to the current working directory. The backend copy is therefore the relevant one for the command below.

Step 5: Start the backend

From the project root, run:

cd backend
uvicorn main:app --reload

Starting from backend/ matches the current relative path used by main.py to load cancer_model.pkl.

When the server is running, visit:

http://127.0.0.1:8000/docs

This opens FastAPI's interactive API documentation.

Startup note: Importing drug_logic.py loads the GDSC CSV and trains its regression model. The first startup may take time. If the dataset cannot be loaded or the required columns are missing, inspect the terminal output.

9. API Endpoints

The following endpoints are present in the provided code:

Method

Endpoint

Purpose

Authentication

POST

/register

Register a user

No

POST

/login

Verify credentials and return a JWT

No

POST

/predict

Return classification and, if applicable, a drug selection

Yes

GET

/my-patients

Retrieve the logged-in user's prediction history

Yes

Register

POST /register accepts JSON:

{
  "username": "sampleuser",
  "password": "samplepassword"
}

The current schema requires a username between 3 and 50 characters and a password of at least 4 characters. Use a strong password even though these are the current minimum validation rules.

Login

POST /login accepts form data with username and password. A successful response contains an access token and the token type bearer.

Predict

POST /predict requires a bearer token and accepts JSON such as:

{
  "radius_mean": 17.0,
  "area_mean": 900.0,
  "radius_worst": 22.0,
  "area_worst": 1400.0,
  "perimeter_mean": 110.0,
  "perimeter_worst": 145.0
}

The response contains a status and confidence percentage, with risk category and recommended drug fields when applicable. This example is only sample input; it does not imply a particular prediction.

Prediction history

GET /my-patients requires a bearer token and returns records belonging to the authenticated user.

10. Database

The backend configures SQLite using sqlite:///./smartcare.db. When the server is started from the backend/ directory, the database is expected at backend/smartcare.db.

SQLAlchemy defines:

users: usernames and hashed passwords.

patients: submitted measurements, diagnosis, confidence, risk category, recommended drug, creation timestamp, and associated user ID.

Keep the database private if it contains real or identifiable data. Use synthetic data for demonstrations.

11. Frontend

The frontend/ directory contains these HTML files:

register.html

login.html

input.html

detection.html

The contents of these pages have not been reviewed here, so the exact navigation flow, styling, and API integration are not documented as confirmed. The backend API can be explored independently at http://127.0.0.1:8000/docs after starting the server.

12. Security and Deployment Notes

jwt_token.py currently contains a hardcoded JWT secret. Do not publish that secret or deploy it as-is. Load a strong secret from an environment variable.

The current CORS configuration allows all origins. Restrict it to the intended frontend origin before deployment.

Use HTTPS and appropriate access controls in a deployed environment.

Do not commit credentials, secrets, or a database containing sensitive information.

Authentication and authorization should be tested before using the application beyond a local demonstration.

13. Limitations and Future Work

Confirm the classifier's class encoding and evaluate it on an independent test set.

Report performance metrics only when supported by actual evaluation results.

Improve the drug-response workflow using appropriate input features and held-out validation.

Validate risk thresholds and recommendation logic scientifically before making any medical claims.

Review frontend/API integration and add automated tests.

Configure secure secrets, CORS, and deployment settings.

14. Conclusion

SMARTCARE demonstrates an integration of a saved machine-learning classifier, a prototype drug-selection workflow, a FastAPI backend, JWT-based authentication, and SQLite persistence. It is a starting point for academic experimentation. Further testing, model validation, and security improvements are needed before any real-world or clinical use.
