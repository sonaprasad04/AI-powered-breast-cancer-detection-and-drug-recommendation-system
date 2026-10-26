from passlib.context import CryptContext

# -----------------------------------------
# PASSWORD CONFIGURATION
# -----------------------------------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# -----------------------------------------
# HASH PASSWORD
# -----------------------------------------
def hash_password(password: str) -> str:
    """
    Hash password using bcrypt
    """

    if not password or password.strip() == "":
        raise ValueError("Password cannot be empty")

    try:
        return pwd_context.hash(password)
    except Exception as e:
        raise RuntimeError(f"Error hashing password: {e}")


# -----------------------------------------
# VERIFY PASSWORD
# -----------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password
    """

    if not plain_password or not hashed_password:
        return False

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
