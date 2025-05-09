from typing import Annotated
from fastapi import FastAPI, Query, Body
from pydantic import BaseModel, AfterValidator, Field
from enum import Enum


class Coordination(BaseModel):
    x: float
    y: float
    z: float | None = None
    description: str
    item_id: float

class Model(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = Field(title="This is an item demonstrating Field and Annotation", max_length=5)
    price: Annotated[int, Field(gt=0, description="The price must be greater than 0"), Field(lt=1000, description="The price must be less than 1000")]
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    return {"item_id": item_id, "item": item}


def valid(arr: list[str]):
    for i in arr:
        if len(i) < 3:
            raise ValueError("Length of each item must be at least 3")

@app.get("/query_validataion")
async def valid(q: Annotated[list[str], Query(min_length=3), AfterValidator(valid)]):
    return {"q": q}

@app.post("/test/{item_id}")
async def test(a_list: list[int], item_id: int, short: bool, xy: Coordination, skip: int = 0, limit: int | None = None, ):
    return {"item_id": item_id, "skip": skip, "limit": limit, 'short': short, "xy": xy, 'list': a_list}

@app.get("/test")
async def test(short: bool, xy: Coordination, skip: int = 0, limit: int | None = None):
    return {"skip": skip, "limit": limit, 'short': short, "xy": xy}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/models/{model}")
async def get_model(model: Model):
    if model == Model.alexnet:
        return {"message": "alexnet here"}
    elif model == Model.resnet:
        return {"message": "some residual"}
    return {"message": "lenet!!!"}

@app.get("/files/{filepath:path}")
async def files(filepath: str):
    return {"filepath": filepath}