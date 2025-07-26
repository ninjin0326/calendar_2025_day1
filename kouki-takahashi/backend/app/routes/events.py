from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models.event import Event
from app.models.user import User
from app.schemas.event import (
    EventCreate,
    EventUpdate,
    EventResponse,
    EventFrontendResponse,
)
from app.routes.auth import verify_credentials

router = APIRouter()


@router.get("/", response_model=List[EventFrontendResponse])
async def get_events(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    # TODO: 課題1 - genreパラメータを追加してください
    genre: Optional[str] = Query(None), # 追加
    username: str = Depends(verify_credentials),
    db: Session = Depends(get_db),
):
    # 現在のユーザーを取得
    current_user = db.query(User).filter(User.username == username).first()
    if not current_user:
        # TODO: 課題3 - エラーメッセージを修正してください
        raise HTTPException(status_code=400, detail="ユーザーが見つかりません")

    # クエリの構築
    query = db.query(Event)

    # ユーザーIDでフィルタ（現在のユーザーのイベントのみ）
    query = query.filter(Event.user_id == current_user.id)

    # 日付範囲でフィルタ
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            query = query.filter(Event.start_datetime >= start_dt)
        except ValueError:
            # TODO: 課題3 - エラーメッセージを修正してください
            raise HTTPException(status_code=400, detail="開始時刻の形式が不正です")

    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            query = query.filter(Event.end_datetime <= end_dt)
        except ValueError:
            # TODO: 課題3 - エラーメッセージを修正してください  
            raise HTTPException(status_code=400, detail="終了時刻の形式が不正です")

    # TODO: 課題1 - ジャンルフィルタを追加してください
    if genre:
        query = query.filter(Event.genre == genre)
    
    events = query.all()

    # フロントエンド互換形式に変換（配列で返す）
    return [EventFrontendResponse.from_event(event) for event in events]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: dict,  # フロントエンドからの形式を受け入れる
    username: str = Depends(verify_credentials),
    db: Session = Depends(get_db),
):
    """イベント作成"""
    # 現在のユーザーを取得
    current_user = db.query(User).filter(User.username == username).first()
    if not current_user:
        raise HTTPException(status_code=400, detail="User not found")

    # ジャンルのバリデーション（事前定義された値のみ許可）
    allowed_genres = ["work", "private", "other"]
    if event_data.get("genre") not in allowed_genres:
        raise HTTPException(
            status_code=400, detail=f"Invalid genre. Allowed values: {allowed_genres}"
        )

    # 簡易的なバリデーション
    start_dt = datetime.fromisoformat(event_data.get("start").replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(event_data.get("end").replace("Z", "+00:00"))

    # フロントエンド形式からバックエンド形式に変換
    new_event = Event(
        title=event_data.get("title"),
        description=event_data.get("description", ""),
        start_datetime=start_dt,
        end_datetime=end_dt,
        all_day=event_data.get("allDay", False),
        genre=event_data.get("genre"),
        user_id=current_user.id,
    )

    db.add(new_event)
    db.commit()

    return None


@router.get("/{event_id}", response_model=EventFrontendResponse)
async def get_event(
    event_id: str,
    username: str = Depends(verify_credentials),
    db: Session = Depends(get_db),
):
    """特定イベント取得"""
    try:
        event_id_int = int(event_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id '{event_id}' not found",
        )

    event = db.query(Event).filter(Event.id == event_id_int).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id '{event_id}' not found",
        )

    # アクセス権限の確認（簡易版）
    current_user = db.query(User).filter(User.username == username).first()
    if event.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this event",
        )

    return EventFrontendResponse.from_event(event)


@router.put("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_event(
    event_id: str,
    event_update: dict,  # フロントエンドからの形式を受け入れる
    username: str = Depends(verify_credentials),
    db: Session = Depends(get_db),
):
    """イベント更新"""
    try:
        event_id_int = int(event_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id '{event_id}' not found",
        )

    event = db.query(Event).filter(Event.id == event_id_int).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id '{event_id}' not found",
        )

    # アクセス権限の確認
    current_user = db.query(User).filter(User.username == username).first()
    if event.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this event",
        )

    # ジャンルのバリデーション
    if "genre" in event_update:
        allowed_genres = ["work", "private", "other"]
        if event_update["genre"] not in allowed_genres:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid genre. Allowed values: {allowed_genres}",
            )

    # 日時のパースとバリデーション
    try:
        if "start" in event_update:
            start_dt = datetime.fromisoformat(
                event_update["start"].replace("Z", "+00:00")
            )
        else:
            start_dt = event.start_datetime

        if "end" in event_update:
            end_dt = datetime.fromisoformat(event_update["end"].replace("Z", "+00:00"))
        else:
            end_dt = event.end_datetime
    except ValueError:
        raise HTTPException(status_code=400, detail="開始時刻または終了時刻が不正です")

    # 更新処理
    if "title" in event_update:
        event.title = event_update["title"]
    if "description" in event_update:
        event.description = event_update["description"]
    if "start" in event_update:
        event.start_datetime = start_dt
    if "end" in event_update:
        event.end_datetime = end_dt
    if "allDay" in event_update:
        event.all_day = event_update["allDay"]
    if "genre" in event_update:
        event.genre = event_update["genre"]

    db.commit()

    return None


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: str,
    username: str = Depends(verify_credentials),
    db: Session = Depends(get_db),
):
    """イベント削除"""
    try:
        event_id_int = int(event_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id '{event_id}' not found",
        )

    event = db.query(Event).filter(Event.id == event_id_int).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id '{event_id}' not found",
        )

    # アクセス権限の確認
    current_user = db.query(User).filter(User.username == username).first()
    if event.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this event",
        )

    db.delete(event)
    db.commit()

    return None
