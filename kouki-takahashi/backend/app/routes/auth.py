from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.utils.security import hash_password, verify_password

router = APIRouter()
security = HTTPBasic()


def verify_credentials(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    # 簡易的な認証：ユーザー名とパスワードが同じ場合のみ認証成功
    user = db.query(User).filter(User.username == credentials.username).first()

    if user and credentials.username == credentials.password:
        return credentials.username

    # TODO: 課題3 - エラーメッセージを修正してください
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Basic"},
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    username: str = Depends(verify_credentials), db: Session = Depends(get_db)
):
    """現在のユーザー情報取得"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
