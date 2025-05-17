from sqlalchemy.orm import Session
from sqlalchemy import select, or_, and_, insert, update, delete

import api_recipes.schemas as schemas
import api_recipes.models as models
from bson.objectid import ObjectId


# CRUD: RECIPES
async def get_all_recipes(db: Session, skip: int = 0, limit: int = 10):
    """Get all recipes
    Args:
        db (Session): _description_
        skip (int, optional): _description_. Defaults to 0.
        limit (int, optional): _description_. Defaults to 10.
    Returns:
        list: _description_
    """
    query_statement = select(models.Recipes).offset(skip).limit(limit)
    result = db.execute(query_statement).scalars().all()
    return result


async def get_recipe_by_id(db: Session, recipe_id: int):
    """Get a recipe by its ID
    Args:
        db (Session): _description_
        recipe_id (int): _description_
    Returns:
        dict: _description_
    """
    query_statement = select(models.Recipes).where(models.Recipes.id == recipe_id)
    result = db.execute(query_statement).scalars().first()
    if result:
        return result
    else:
        return None


# Search
async def search_recipes_by_day(db: Session, day: str):
    """Search for an item in the collection by ID
    Args:
        item_id (str): _description_
    Returns:
        dict: _description_
    """
    query_statement = select(models.WeekPlan).where(
        or_(
            models.WeekPlan.day.ilike(f"%{day}%"),
        )
    )

    result = db.execute(query_statement).scalars().all()

    if result:
        return result
    else:
        return None


# CREATE


async def create_recipe(
    db: Session, recipe: schemas.Recipe, ingredients: list[schemas.Ingredient]
):
    """Create a new recipe
    Args:
        db (Session): _description_
        recipe (schemas.Recipe): _description_
    Returns:
        dict: _description_
    """
    new_recipe = models.Recipes(**recipe.dict())
    for ingredients in ingredients:
        new_recipe.ingredients.append(
            models.Ingredient(
                name=recipe.ingredient.name,
                base_price=recipe.ingredient.base_price,
                source=recipe.ingredient.source,
                additional_info=recipe.ingredient.additional_info,
            )
        )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


async def create_ingredient(db: Session, ingredient: schemas.Ingredient):
    """Create a new ingredient
    Args:
        db (Session): _description_
        ingredient (schemas.Ingredient): _description_
    Returns:
        dict: _description_
    """
    new_ingredient = models.Ingredient(**ingredient.dict())
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient
