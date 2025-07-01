from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Event).order_by(Event.start_dt).offset(skip).limit(limit).all()

def get_event(db: Session, event_id: int):
    return db.query(Event).filter(Event.event_id == event_id).first()

def create_event(db: Session, in_e: EventCreate):
    db_obj = Event(**in_e.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_event(db: Session, eid: int, in_e: EventUpdate):
    obj = get_event(db, eid)
    if not obj:
        return None
    for field, value in in_e.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_event(db: Session, eid: int):
    obj = get_event(db, eid)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
