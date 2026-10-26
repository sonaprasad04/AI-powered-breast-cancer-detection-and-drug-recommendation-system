from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import User
from security import hash_password, verify_password
from jwt_token import create_token
from schemas import UserCreate

router = APIRouter()


# -----------------------------------
# REGISTER API (JSON)
# -----------------------------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    print("📥 Register request:", user.username)

    # Check if user already exists
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        print("❌ User already exists")
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    # Create new user
    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print("✅ User registered:", new_user.username)

    return {
        "message": "User registered successfully"
    }


# -----------------------------------
# LOGIN API (FORM DATA)
# -----------------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    print("📥 Login attempt:", form_data.username)

    # Find user
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    # Validate user
    if not user:
        print("❌ User not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Validate password
    if not verify_password(form_data.password, user.password):
        print("❌ Wrong password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create token (IMPORTANT)
    token = create_token(user.id)

    print("✅ Login success:", user.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
