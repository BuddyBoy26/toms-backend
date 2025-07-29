from sqlalchemy.orm import Session
from app.models.log import Log as LogModel
from app.schemas.log import LogCreate

def create_log(db: Session, log_in: LogCreate, user_id: int) -> LogModel:
    db_log = LogModel(**log_in.dict(), user_id=user_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_log(db: Session, log_id: int) -> LogModel | None:
    return db.query(LogModel).filter(LogModel.id == log_id).first()

def get_logs(db: Session, skip: int = 0, limit: int = 100) -> list[LogModel]:
    return db.query(LogModel).offset(skip).limit(limit).all()
