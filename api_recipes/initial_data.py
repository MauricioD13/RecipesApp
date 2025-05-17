from sqlalchemy import insert
from sqlalchemy.orm import Session

from pydantic_core import from_json

import app.models as models
import app.schemas as schemas
import app.crud as crud
import json


def insert_data():
    ingredients = [
        {
            "_id": 1,
            "name": "Pasta",
            "base_price": "2.00",
            "source": "Italy",
            "additional_info": "Whole wheat pasta",
        },
        {
            "_id": 2,
            "name": "Tomato Sauce",
            "base_price": "1.50",
            "source": "Italy",
            "additional_info": "Organic tomato sauce",
        },
        {
            "_id": 3,
            "name": "Cheese",
            "base_price": "3.00",
            "source": "Italy",
            "additional_info": "Parmesan cheese",
        },
    ]
    market_prices = [
        {
            "_id": 1,
            "ingredient_id": 1,
            "price": "2.00",
            "date": "2023-10-01",
            "market_name": "Local Market",
        },
        {
            "_id": 2,
            "ingredient_id": 2,
            "price": "1.50",
            "date": "2023-10-01",
            "market_name": "Local Market",
        },
        {
            "_id": 3,
            "ingredient_id": 3,
            "price": "3.00",
            "date": "2023-10-01",
            "market_name": "Local Market",
        },
    ]
    recipes = [
        {
            "name": "Pasta",
            "description": "Delicious pasta with tomato sauce",
            "ingredients": ["pasta", "tomato sauce", "cheese"],
            "instructions": ["Boil pasta", "Add sauce", "Serve with cheese"],
            "image_url": "http://example.com/pasta.jpg",
            "preparation_time": 30,
            "portions": 4,
            "tags": ["Italian", "Main Course"],
        },
        {
            "name": "Salad",
            "description": "Fresh salad with vegetables",
            "ingredients": ["lettuce", "tomato", "cucumber"],
            "instructions": ["Chop vegetables", "Mix together", "Serve"],
            "image_url": "http://example.com/salad.jpg",
            "preparation_time": 15,
            "portions": 2,
            "tags": ["Healthy", "Appetizer"],
        },
        {
            "name": "Pizza",
            "description": "Cheesy pizza with pepperoni",
            "ingredients": ["dough", "cheese", "pepperoni"],
            "instructions": ["Prepare dough", "Add toppings", "Bake"],
            "image_url": "http://example.com/pizza.jpg",
            "preparation_time": 45,
            "portions": 4,
            "tags": ["Italian", "Main Course"],
        },
    ]
    user = {"_id": 1, "email": "test@example.com"}
    weekplans = [
        {
            "_id": 1,
            "meal": "Lunch",
            "day": "Monday",
            "recipe_id": 1,
            "recipe_name": "Pasta",
        },
        {
            "_id": 2,
            "meal": "Dinner",
            "day": "Monday",
            "recipe_id": 2,
            "recipe_name": "Salad",
        },
        {
            "_id": 3,
            "meal": "Breakfast",
            "day": "Tuesday",
            "recipe_id": 3,
            "recipe_name": "Pizza",
        },
        {
            "_id": 4,
            "meal": "Breakfast",
            "day": "Monday",
            "recipe_id": 1,
            "recipe_name": "Pasta",
        },
        {
            "_id": 5,
            "meal": "Dinner",
            "day": "Tuesday",
            "recipe_id": 2,
            "recipe_name": "Salad",
        },
        {
            "_id": 6,
            "meal": "Breakfast",
            "day": "Wednesday",
            "recipe_id": 3,
            "recipe_name": "Pizza",
        },
        {
            "_id": 7,
            "meal": "Lunch",
            "day": "Wednesday",
            "recipe_id": 1,
            "recipe_name": "Pasta",
        },
        {
            "_id": 8,
            "meal": "Dinner",
            "day": "Wednesday",
            "recipe_id": 2,
            "recipe_name": "Salad",
        },
    ]
    ingredients_objs = []
    for ingredient in ingredients:
        ingredient_model = schemas.Ingredient.model_validate(
            from_json(json.dumps(ingredient))
        )
        ingredients_objs.append(
            crud.create_ingredient(ingredient_model=ingredient_model)
        )

    for recipe in recipes:
        recipe_model = schemas.Recipe.model_validate(from_json(json.dumps(recipe)))

        crud.create_recipe(recipe_model=recipe_model, ingredients=ingredients_objs)
