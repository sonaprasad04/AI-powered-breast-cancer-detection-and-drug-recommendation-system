from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

# -----------------------------------------
# SECRET CONFIGURATION
# -----------------------------------------
SECRET_KEY = "mysecretkey123"   # change for production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# -----------------------------------------
# CREATE ACCESS TOKEN
# -----------------------------------------
def create_token(user_id: int):
    """
    Create JWT token for a user
    """

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),   # user id
        "exp": expire
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


# -----------------------------------------
# DECODE / VERIFY TOKEN
# -----------------------------------------
def decode_token(token: str):
    """
    Decode JWT token and return user_id
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except JWTError:
        return None
