from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------------------
# DATABASE CONFIGURATION
# -----------------------------------------

# SQLite database file
DATABASE_URL = "sqlite:///./smartcare.db"

# -----------------------------------------
# ENGINE
# -----------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required only for SQLite
)

# -----------------------------------------
# SESSION
# -----------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------------------
# BASE MODEL
# -----------------------------------------
Base = declarative_base()


# -----------------------------------------
# DATABASE DEPENDENCY (IMPORTANT)
# -----------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
