# --- crud/arena.py ---
from sqlalchemy.orm import Session
from models.arena import Arena
import uuid

def create_arena(db: Session, title: str, address: str, capacity: int) -> Arena:
    arena = Arena(
        id=uuid.uuid4(),
        title=title,
        address=address,
        capacity=capacity
    )
    db.add(arena)
    db.commit()
    db.refresh(arena)
    return arena

def get_all_arenas(db: Session):
    return db.query(Arena).all()

def get_arena_by_id(db: Session, arena_id: str):
    return db.query(Arena).filter_by(id=arena_id).first()