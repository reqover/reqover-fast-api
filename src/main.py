import os

import uvicorn as uvicorn
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}


class Item(BaseModel):
    id: str
    title: str
    description: str = None


fake_secret_token = "coneofsilence"

app = FastAPI()


@app.get("/status", deprecated=True)
def read_root():
    return {"status": "ok"}


@app.get("/items/{item_id}", response_model=Item,
         responses={404: {"description": "Item not found"}, 400: {"description": "Invalid X-Token header"}})
def get_item_by_id(item_id: str, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id] = item
    return item


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))
