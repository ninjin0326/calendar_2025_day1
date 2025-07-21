"""データベース初期化スクリプト"""

from app.database import SessionLocal, create_tables
from app.models.user import User
from app.models.event import Event
from app.utils.security import hash_password
from datetime import datetime, timedelta
import pytz


def init_db():
    """データベースを初期化し、サンプルデータを投入"""
    # テーブルを作成
    create_tables()

    # セッションを作成
    db = SessionLocal()

    try:
        # 既存のデータをクリア
        db.query(Event).delete()
        db.query(User).delete()
        db.commit()

        # サンプルユーザーを作成
        users = [
            User(
                username="testuser",
                email="testuser@example.com",
                password_hash=hash_password("testuser"),
            ),
        ]

        for user in users:
            db.add(user)

        db.commit()

        # サンプルイベントを作成
        jst = pytz.timezone("Asia/Tokyo")
        now = datetime.now(jst)

        events = [
            Event(
                title="チーム会議",
                description="週次の進捗確認ミーティング",
                start_datetime=now.replace(hour=10, minute=0, second=0, microsecond=0),
                end_datetime=now.replace(hour=11, minute=0, second=0, microsecond=0),
                genre="work",
                all_day=False,
                user_id=1,
            ),
            Event(
                title="プロジェクト企画会議",
                description="新規プロジェクトの企画会議",
                start_datetime=(now + timedelta(days=1)).replace(
                    hour=14, minute=0, second=0, microsecond=0
                ),
                end_datetime=(now + timedelta(days=1)).replace(
                    hour=16, minute=0, second=0, microsecond=0
                ),
                genre="work",
                all_day=False,
                user_id=1,
            ),
            Event(
                title="外出",
                description="A社への定例訪問",
                start_datetime=(now + timedelta(days=2)).replace(
                    hour=13, minute=0, second=0, microsecond=0
                ),
                end_datetime=(now + timedelta(days=2)).replace(
                    hour=15, minute=0, second=0, microsecond=0
                ),
                genre="work",
                all_day=False,
                user_id=1,
            ),
            Event(
                title="休暇",
                description="有給休暇",
                start_datetime=(now + timedelta(days=5)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                ),
                end_datetime=(now + timedelta(days=5)).replace(
                    hour=23, minute=59, second=59, microsecond=0
                ),
                genre="private",
                all_day=True,
                user_id=1,
            ),
        ]

        for event in events:
            db.add(event)

        db.commit()
        print("データベースの初期化が完了しました。")
        print(f"ユーザー数: {db.query(User).count()}")
        print(f"イベント数: {db.query(Event).count()}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
