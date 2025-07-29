from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.drawing_details import DrawingDetails
from app.schemas.drawing_details import DrawingDetailsCreate

def create_drawing_details(
    db: Session,
    dd_in: DrawingDetailsCreate
) -> DrawingDetails:
    db_dd = DrawingDetails(**dd_in.dict())
    db.add(db_dd)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A drawing record for this tender_no and order_id already exists."
        )
    db.refresh(db_dd)
    return db_dd

def get_drawing_details(db: Session, dd_id: int) -> DrawingDetails | None:
    return db.query(DrawingDetails).filter(DrawingDetails.id == dd_id).first()

def list_drawing_details(
    db: Session, skip: int = 0, limit: int = 100
) -> list[DrawingDetails]:
    return db.query(DrawingDetails).offset(skip).limit(limit).all()

def update_drawing_details(
    db: Session, dd_id: int, dd_in: DrawingDetailsCreate
) -> DrawingDetails:
    db_dd = get_drawing_details(db, dd_id)
    if not db_dd:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    for field, val in dd_in.dict().items():
        setattr(db_dd, field, val)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Composite key conflict on update."
        )
    db.refresh(db_dd)
    return db_dd

def delete_drawing_details(db: Session, dd_id: int) -> None:
    db_dd = get_drawing_details(db, dd_id)
    if not db_dd:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(db_dd)
    db.commit()
