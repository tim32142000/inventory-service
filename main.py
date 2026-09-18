from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from models import ItemCreate, ItemResponse
from database_models import Item

from database import (
    init_db,
    get_list_items,
    delete_item,
)

from service import (
    create_item_service,
    get_list_items_service,
    get_item_service,
    update_item_service,
    delete_item_service,
)

from exceptions import BusinessRuleError, ItemNotFoundError


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(BusinessRuleError)
async def handle_bussiness_rule_error(request: Request, exc: BusinessRuleError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(ItemNotFoundError)
async def handle_item_not_found_error(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.get("/")
def root():
    return {"message": "Item API is running"}


@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item_api(item: ItemCreate):
    db_item = Item(
        name=item.name,
        category=item.category,
        price=item.price,
        quantity=item.quantity,
    )

    return create_item_service(db_item)


@app.get("/items", response_model=list[ItemResponse])
def get_list_items_api(category: str|None = None):
    return get_list_items_service(category)


@app.get("/items/{id}", response_model=ItemResponse)
def get_item_api(id: int):
    row = get_item_service(id)

    return row


@app.delete(
    "/items/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item_api(id: int):
    delete_item_service(id)


@app.put("/items/{id}", response_model=ItemResponse)
def update_item_api(id: int, item: ItemCreate):
    db_item = Item(
        id=id,
        name=item.name,
        category=item.category,
        price=item.price,
        quantity=item.quantity,
    )

    updated_item = update_item_service(db_item)

    return updated_item
