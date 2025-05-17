import pytest
from fastapi.testclient import TestClient
import os
from tests.test_config import init_test_db, cleanup_test_db, override_get_db
from main import app, get_db

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

user_data = {
            "email": "testuser@example.com",
            "password": "testpassword"
}

recipe_data = {
            "description": "Delicious test recipe",
            "ingredients": "ingredient1, ingredient2",
            "steps": "Step 1, Step 2",
            "duration": 30
}

@pytest.fixture(autouse=True)
def setup_db():
    init_test_db()
    yield
    cleanup_test_db()
    # Sample test data



@pytest.fixture
def setup_user():
    # Create a test user in the database
    response = client.post("/signup", json=user_data)
    assert response.status_code == 200
    return response.json()


# Test cases
def test_signup_user():
    response = client.post("/signup", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]


def test_signup_duplicate_user():
    client.post("/signup", json=user_data)  # Create user
    response = client.post("/signup", json=user_data)  # Duplicate user
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

duration
def test_get_user_by_id(setup_user):
    user_id = setup_user["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200


def test_create_recipe_for_user(setup_user):
    user_id = setup_user["id"]
    response = client.post(f"/users/{user_id}/recipes/", json=recipe_data)
    assert response.status_code == 200
    print(response.json())
    assert response. json()["duration"] == recipe_data["duration"]


def test_get_recipes():
    response = client.get("/recipe/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
