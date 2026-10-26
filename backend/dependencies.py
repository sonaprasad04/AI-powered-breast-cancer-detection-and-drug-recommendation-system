from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from jwt_token import decode_token
from models import User

# -----------------------------------------
# TOKEN SCHEME (READ FROM HEADER)
# -----------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# -----------------------------------------
# GET CURRENT USER FROM TOKEN
# -----------------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Extract user from JWT token
    """

    # ---------------------------
    # STEP 1: DECODE TOKEN
    # ---------------------------
    user_id = decode_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # ---------------------------
    # STEP 2: GET USER FROM DB
    # ---------------------------
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # ---------------------------
    # STEP 3: RETURN USER
    # ---------------------------
    return user
