import ssl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

# Configure engine based on database URL
db_url = settings.database_url
connect_args = {}

if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
elif db_url.startswith("postgresql://"):
    # Use pg8000 pure-Python driver
    # Strip query params not supported by pg8000 before replacing dialect
    base_url = db_url.split("?")[0]
    db_url = base_url.replace("postgresql://", "postgresql+pg8000://", 1)
    # Enable SSL for NeonDB (and any remote PostgreSQL)
    ssl_context = ssl.create_default_context()
    connect_args = {"ssl_context": ssl_context}

engine = create_engine(
    db_url,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
