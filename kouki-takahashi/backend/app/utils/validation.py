# TODO: 課題4 - イベント重複チェック機能を実装してください
# check_event_overlap関数を実装してください

from sqlalchemy.orm import Session
from app.models.event import Event
from datetime import datetime  

def check_event_overlap(
    db: Session,
    user_id: int,
    start_datetime: str,
    end_datetime: str,
) -> bool:
    """指定された期間にイベントが重複しているか確認する"""
    overlapping_event = db.query(Event).filter(
        Event.user_id == user_id,
        Event.start_datetime < end_datetime,
        Event.end_datetime > start_datetime,
    ).first()
    
    return overlapping_event is not None