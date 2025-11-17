from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import History
from datetime import datetime
from ..schemas.history import HistoryCreate, HistoryResponse
from sqlalchemy import func, cast, Date



router = APIRouter(
    prefix="/history",
    tags=["History"],
)

@router.post("/")
def create_history(
    data: HistoryCreate,
    db: Session = Depends(get_db)
):
    history = History(
        ImageUrl = data.image_url,
        CreatedDate = datetime.utcnow(),
        UID = data.uid,
        Status = data.status
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return {
        "message": "History created successfully",
        "data": {
            "id": history.HistoryId,
            "image_url": history.ImageUrl,
            "created_date": history.CreatedDate,
            "status": history.Status,
            "uid": history.UID
        }
    }

@router.get("/grouped-by-date")
def get_history_grouped_by_date(db: Session = Depends(get_db)):
    # Query all records ordered by newest first
    rows = (
        db.query(
            cast(History.CreatedDate, Date).label("date"),
            History
        )
        .order_by(History.CreatedDate.desc())
        .all()
    )

    grouped = {}

    for date_value, record in rows:
        date_str = date_value.isoformat()  # convert to "YYYY-MM-DD"
        if date_str not in grouped:
            grouped[date_str] = []
        
        grouped[date_str].append({
            "HistoryId": record.HistoryId,
            "ImageUrl": record.ImageUrl,
            "CreatedDate": record.CreatedDate,
            "Status": record.Status,
            "UID": record.UID
        })

    return grouped