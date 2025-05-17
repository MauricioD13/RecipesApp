from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    TIMESTAMP,
    text,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.mysql import VARCHAR
from typing import Optional, List

from datetime import datetime, timezone
from api_recipes.database import Base


class Recipes(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    make_time: Mapped[Optional[int]] = mapped_column(String(50), default=None)
    steps: Mapped[Optional[str]] = mapped_column(String(5000), default=None)
    image_url: Mapped[Optional[str]] = mapped_column(String(1000), default=None)
    portions: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    tags: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    # Relationships
    ingredients: Mapped[List["RecipesIngredients"]] = relationship(
        back_populates="recipes", cascade="all, delete-orphan"
    )
    week_plan: Mapped[List["WeekPlan"]] = relationship(
        "WeekPlan", back_populates="recipes", cascade="all, delete-orphan"
    )
    # Association proxy to access ingredients directly
    ingredients_list: Mapped[List["Ingredients"]] = association_proxy(
        "ingredients", "ingredient"
    )


class Ingredients(Base):
    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String(100))
    base_price: Mapped[Optional[str]] = mapped_column(String(50))
    source: Mapped[Optional[str]] = mapped_column(String(50))
    additional_info: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    # updated_at: Mapped[datetime] = mapped_column(
    #    TIMESTAMP,
    #    server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    #    nullable=False,
    # )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # DEFAULT CURRENT_TIMESTAMP  (SQLite-friendly)
        onupdate=func.now(),  # SQLAlchemy sets NEW value on every UPDATE
        nullable=False,
    )
    # Relationships
    market_price: Mapped["MarketPrices"] = relationship(
        "MarketPrices", back_populates="price_ingredients", cascade="all, delete-orphan"
    )
    recipes_ingredients: Mapped[List["RecipesIngredients"]] = relationship(
        back_populates="ingredients", cascade="all, delete-orphan"
    )
    # Association proxy to access recipes directly
    recipes_list: Mapped[List["Recipes"]] = association_proxy(
        "recipes_ingredients", "recipe"
    )


class RecipesIngredients(Base):
    __tablename__ = "recipes_ingredients"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey("recipes.id"))
    ingredient_id: Mapped[int] = mapped_column(Integer, ForeignKey("ingredients.id"))
    quantity: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    # updated_at: Mapped[datetime] = mapped_column(
    #    TIMESTAMP,
    #    server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    #    nullable=False,
    # )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # DEFAULT CURRENT_TIMESTAMP  (SQLite-friendly)
        onupdate=func.now(),  # SQLAlchemy sets NEW value on every UPDATE
        nullable=False,
    )
    # Relationships
    recipes: Mapped["Recipes"] = relationship("Recipes", back_populates="ingredients")
    ingredients: Mapped["Ingredients"] = relationship(
        "Ingredients", back_populates="recipes_ingredients"
    )


class MarketPrices(Base):
    __tablename__ = "market_prices"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    ingredient_id: Mapped[int] = mapped_column(Integer, ForeignKey("ingredients.id"))
    price: Mapped[Optional[str]] = mapped_column(String(50))
    date: Mapped[Optional[str]] = mapped_column(String(50))
    market_name: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    # updated_at: Mapped[datetime] = mapped_column(
    #    TIMESTAMP,
    #    server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    #    nullable=False,
    # )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # DEFAULT CURRENT_TIMESTAMP  (SQLite-friendly)
        onupdate=func.now(),  # SQLAlchemy sets NEW value on every UPDATE
        nullable=False,
    )
    __table_args__ = (
        UniqueConstraint(
            "ingredient_id", "market_name", "price", name="uq_ingredient_date_market"
        ),
    )
    # Relationships
    price_ingredients: Mapped["Ingredients"] = relationship(
        "Ingredients", back_populates="market_price"
    )


class WeekPlan(Base):
    __tablename__ = "week_plan"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    meal: Mapped[Optional[str]] = mapped_column(String(50))
    day: Mapped[Optional[str]] = mapped_column(String(50))
    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey("recipes.id"))
    submitted_by: Mapped[Optional[str]] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    # updated_at: Mapped[datetime] = mapped_column(
    #    TIMESTAMP,
    #    server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    #    nullable=False,
    # )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # DEFAULT CURRENT_TIMESTAMP  (SQLite-friendly)
        onupdate=func.now(),  # SQLAlchemy sets NEW value on every UPDATE
        nullable=False,
    )
    __table_args__ = (UniqueConstraint("meal", "day", name="uq_meal_day"),)

    # Relationships
    recipes: Mapped["Recipes"] = relationship("Recipes", back_populates="week_plan")
