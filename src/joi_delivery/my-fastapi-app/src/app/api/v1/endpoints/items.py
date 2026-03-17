from fastapi import APIRouter, HTTPException
from src.app.models.item import Item
from src.app.schemas.item import ItemCreate, ItemUpdate

router = APIRouter()

items_db = {}

@router.post("/", response_model=Item)
def create_item(item: ItemCreate):
    item_id = len(items_db) + 1
    new_item = Item(id=item_id, **item.dict())
    items_db[item_id] = new_item
    return new_item

@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = items_db[item_id].copy(update=item.dict())
    items_db[item_id] = updated_item
    return updated_item

@router.delete("/{item_id}", response_model=Item)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)
    return deleted_item