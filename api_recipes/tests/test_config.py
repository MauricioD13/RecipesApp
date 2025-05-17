import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create test SessionLocal
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables for test database
def init_test_db():
    Base.metadata.create_all(bind=engine)

# Cleanup test database
def cleanup_test_db():
    Base.metadata.drop_all(bind=engine)

# Override the original database settings
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

