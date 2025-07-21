from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.routes.auth import verify_credentials

router = APIRouter()


@router.get("/", response_model=List[str])
async def get_users(
    username: str = Depends(verify_credentials), db: Session = Depends(get_db)
):
    """ユーザー一覧取得"""
    users = db.query(User).all()

    # ユーザー名の配列を返す
    return [user.username for user in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    username: str = Depends(verify_credentials),
    db: Session = Depends(get_db),
):
    """特定ユーザー取得"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found",
        )

    return user
