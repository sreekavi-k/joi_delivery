from fastapi import Depends
from sqlalchemy.orm import Session
from .core.config import get_db

def get_items_db(db: Session = Depends(get_db)):
    return db.query(Item).all()  # Example function to get items from the database

# Add more dependency functions as needed for your application