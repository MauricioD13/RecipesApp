from pydantic import BaseModel
from typing import Annotated, Literal
from datetime import date


class RecipeBase(BaseModel):
    _id: int
    name: str
    description: str
    ingredients: list[str]
    instructions: list[str]
    preparation_time: int
    portions: int
    image_url: str
    tags: str


class Ingredient(BaseModel):
    name: str
    base_price: str
    source: str
    additional_info: str


class WeekPlan(BaseModel):
    id: int
    meal: Literal["Breakfast", "Lunch", "Dinner"]
    day: Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    recipe_id: int
    submitted_by: str


class User(BaseModel):
    _id: int
    email: str
    created_at: date
    updated_at: date


class Recipe(RecipeBase):
    pass
