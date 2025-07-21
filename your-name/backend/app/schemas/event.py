from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.user import UserResponse


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    all_day: bool = False
    genre: str


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    all_day: Optional[bool] = None
    genre: Optional[str] = None


class EventResponse(EventBase):
    id: int
    user_id: int
    user: UserResponse
    created_at: datetime
    updated_at: datetime
    # TODO: 課題5 - duration_minutesフィールドを追加してください

    class Config:
        from_attributes = True


# フロントエンド互換性のためのスキーマ
class EventFrontendResponse(BaseModel):
    """フロントエンドが期待する形式のイベントレスポンス"""

    id: str
    title: str
    start: str  # ISO 8601形式
    end: str  # ISO 8601形式
    genre: str
    allDay: bool
    users: Optional[List[str]] = None
    # TODO: 課題5 - duration_minutesフィールドを追加してください

    @classmethod
    def from_event(cls, event):
        return cls(
            id=str(event.id),
            title=event.title,
            start=event.start_datetime.isoformat(),
            end=event.end_datetime.isoformat(),
            genre=event.genre,
            allDay=event.all_day,
            users=[event.user.username] if event.user else [],
        )
