import uuid
from datetime import datetime, date
from sqlalchemy.orm import Session
from models.activity import Activity
from models.arena import Arena
from models.arena_taken import ArenaTaken

def create_activity(
    db: Session,
    title: str,
    content: str,
    price: int,
    on_sale_date: datetime,
    start_time: datetime,
    end_time: datetime,
    cover_image: str,
    arena_id: uuid.UUID,
    creator_id: uuid.UUID,
    num_ticket: int,
) -> Activity:
    activity = Activity(
        id=uuid.uuid4(),
        title=title,
        content=content,
        price=price,
        on_sale_date=on_sale_date,
        start_time=start_time,
        end_time=end_time,
        cover_image=cover_image,
        arena_id=arena_id,
        creator_id=creator_id,
        num_ticket=num_ticket,
        is_achieved=False,
    )
    db.add(activity)
    db.flush()  # to get activity.id before commit
    return activity

def get_activity_by_id(db: Session, activity_id: uuid.UUID) -> Activity | None:
    return db.query(Activity).filter_by(id=activity_id).first()

def get_all_activities(db: Session) -> list[Activity]:
    return db.query(Activity).all()

def get_activities_by_creator(db: Session, creator_id: uuid.UUID) -> list[Activity]:
    return db.query(Activity).filter_by(creator_id=creator_id).all()

def update_activity(db: Session, activity: Activity, update_data: dict) -> None:
    # update_data keys may include title, content, price, on_sale_date, start_time, end_time, cover_image
    for key, value in update_data.items():
        setattr(activity, key, value)
    db.commit()

def is_arena_available(db: Session, arena_id: uuid.UUID, date_to_check: date) -> bool:
    taken = db.query(ArenaTaken).filter_by(arena_id=arena_id, date=date_to_check).first()
    return taken is None

def create_arena_taken(db: Session, activity_id: uuid.UUID, arena_id: uuid.UUID, date_taken: date) -> ArenaTaken:
    arena_taken = ArenaTaken(
        id=uuid.uuid4(),
        activity_id=activity_id,
        arena_id=arena_id,
        date=date_taken,
    )
    db.add(arena_taken)
    return arena_taken
