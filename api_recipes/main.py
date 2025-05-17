# FastAPI Imports
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

# Local Imports
import api_recipes.crud as crud
from api_recipes.database import get_db, Base, engine
import api_recipes.schemas as schemas
import api_recipes.models as models
from api_recipes.misc import parsed_sql_pydantic

import asyncio


app = FastAPI()
counter = 0
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)


@app.get("/api/v1/read-user", response_class=HTMLResponse)
async def get_user(request: Request, item_id: str):
    user = crud.get_item(item_id=item_id, collection=app.mongodb["users"])
    return templates.TemplateResponse(request, name="signup.html")


# HTML ENDPOINTS
@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(request, name="home.html")


@app.get("/weekplan", response_class=HTMLResponse)
async def read_weekplan(request: Request, db: Session = Depends(get_db)):
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    weekplan_days = {}
    for day in weekdays:
        weekplan_entries = await crud.search_recipes_by_day(db=db, day=day)
        recipes = []
        if weekplan_entries:
            for weekplan_entry in weekplan_entries:
                recipe_model = await crud.get_recipe_by_id(
                    db=db, recipe_id=weekplan_entry.recipe_id
                )
                recipe = parsed_sql_pydantic(recipe_model, schemas.Recipe)
                recipes.append(recipe)
            weekplan_days[day] = recipes
        else:
            weekplan_days[day] = [""]
    option_recipes = await crud.get_all_recipes(
        db=db, skip=0, limit=10
    )  # Adjust the limit as needed

    return templates.TemplateResponse(
        request,
        name="weekplan.html",
        context={"weekplan_days": weekplan_days, "option_recipes": option_recipes},
    )


@app.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    result = await crud.test_items()
    print(f"Test Items: {result}")
    return templates.TemplateResponse(
        request, name="test.html", context={"result": result}
    )


@app.get("/edit-weekplan-entry/{entry_id}", response_class=HTMLResponse)
async def edit_weekplan_entry(request: Request, entry_id: str):
    weekplan_entry = await crud.get_item(entry_id, collection=app.mongodb["weekplan"])
    if not weekplan_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    recipes = await crud.get_items(0, 10, collection=app.mongodb["recipes"])
    return templates.TemplateResponse(
        request,
        name="edit_weekplan_entry.html",
        context={"weekpla_entry": weekplan_entry, "recipes": recipes},
    )


@app.post("/update-weekplan-entry", response_class=HTMLResponse)
async def update_weekplan_entry(
    request: Request, recipe_id: str = Form(...), weekplan_entry: str = Form(...)
):
    print(f"Recipe ID: {recipe_id}")
    print(f"Weekplan Entry ID: {weekplan_entry}")
    weekplan_entry_obj = await crud.get_item("1", collection=app.mongodb["weekplan"])
    print(f"Weekplan Entry Object: {weekplan_entry_obj}")
    weekplan_entry_obj = None
    if not weekplan_entry_obj:
        raise HTTPException(status_code=404, detail="Entry not found")
    weekplan_entry_obj["recipe_id"] = recipe_id
    await crud.update_item(
        weekplan_entry,
        collection=app.mongodb["weekplan"],
        schema_validator=schemas.WeekplanEntry,
    )
    return RedirectResponse(url="/weekplan", status_code=303)
