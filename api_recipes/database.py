# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# FastAPI
from fastapi import FastAPI

# import motor.motor_asyncio

# from contextlib import asynccontextmanager

import os
import json

param_names = [
    "/myapp/prod/db_username",
    "/myapp/prod/db_password",
    "/myapp/prod/db_endpoint",
]

# params = aws_config.get_parameters(param_names, region="eu-west-1")

# environment = os.environ["ENVIRONMENT"
environment = "dev"
if environment == "dev":
    engine = create_engine(
        "sqlite:///./sql_app.db", connect_args={"check_same_thread": False}
    )
elif environment == "prod":
    USERNAME = os.environ["DB_USER"]
    PASSWORD = os.environ["DB_PASS"]
    HOST = os.environ["DB_HOST"]
    DATABASE = os.environ["DB_NAME"]
    PORT = 3306
    DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
MONGO_URI = "mongodb://root:example@localhost:27017"


def recipe_helper(recipe) -> dict:
    return {
        "id": str(recipe["_id"]),
        "user_id": str(recipe["user_id"]),
        "name": recipe["name"],
        "description": recipe["description"],
        "ingredients": recipe["ingredients"],
        "Createtags": recipe["tags"],
    }


def weekplan_helper(weekplan) -> dict:
    return {
        "id": str(weekplan["_id"]),
        "meal": weekplan["meal"],
        "day": weekplan["day"],
        "recipe_id": weekplan["recipe_id"],
        "recipe_name": weekplan["recipe_name"],
    }


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client(app)
    yield
    await shutdown_db_client(app)


async def startup_db_client(app: FastAPI):
    app.db_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    app.mongodb = app.db_client.get_database("recipe-app-db")
    print("Connected to MongoDB")


async def shutdown_db_client(app: FastAPI):
    app.db_client.close()
"""
