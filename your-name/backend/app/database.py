from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# データベースURL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./calendar.db")

# SQLAlchemyエンジン
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

# セッションローカル
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラス
Base = declarative_base()


def get_db():
    """データベースセッションの依存性注入用関数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """全てのテーブルを作成"""
    from app.models import user, event  # 循環インポート回避

    Base.metadata.create_all(bind=engine)
