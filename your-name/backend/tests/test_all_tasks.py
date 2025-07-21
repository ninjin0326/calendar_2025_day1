"""
全ての課題が正しく実装されたことを検証するテスト
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import time
import sqlite3
import base64
from app.main import app

client = TestClient(app)


def create_basic_auth_header(username: str, password: str) -> dict:
    """Basic認証用のヘッダーを作成"""
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return {"Authorization": f"Basic {encoded_credentials}"}


class TestTask1GenreFilter:
    """課題1: ジャンルフィルタ機能の検証"""

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """テスト用データの準備"""
        # テスト用ユーザー（testuser:testuser）でBasic認証
        self.username = "testuser"
        self.password = "testuser"
        self.headers = create_basic_auth_header(self.username, self.password)

        # work, private の各ジャンルのイベントを作成
        events = [
            {
                "title": "Work Event 1",
                "description": "Work event",
                "start": "2024-01-01T10:00:00",
                "end": "2024-01-01T11:00:00",
                "allDay": False,
                "genre": "work"
            },
            {
                "title": "Work Event 2",
                "description": "Another work event",
                "start": "2024-01-02T10:00:00",
                "end": "2024-01-02T11:00:00",
                "allDay": False,
                "genre": "work"
            },
            {
                "title": "Private Event 1",
                "description": "Private event",
                "start": "2024-01-03T10:00:00",
                "end": "2024-01-03T11:00:00",
                "allDay": False,
                "genre": "private"
            }
        ]

        for event in events:
            response = client.post("/api/events/", json=event, headers=self.headers)
            assert response.status_code == 201

    def test_get_all_events_without_filter(self):
        """フィルタなしで全件取得できることを確認"""
        response = client.get("/api/events/", headers=self.headers)
        assert response.status_code == 200
        events = response.json()
        # 新しく作成したイベント+既存のサンプルイベントがあるため3以上
        assert len(events) >= 3

    def test_filter_by_work_genre(self):
        """workジャンルのフィルタが正しく動作することを確認"""
        response = client.get("/api/events/?genre=work", headers=self.headers)
        assert response.status_code == 200
        events = response.json()

        # 全てのイベントがworkジャンルであることを確認
        assert len(events) >= 2
        for event in events:
            assert event["genre"] == "work"

    def test_filter_by_private_genre(self):
        """privateジャンルのフィルタが正しく動作することを確認"""
        response = client.get("/api/events/?genre=private", headers=self.headers)
        assert response.status_code == 200
        events = response.json()

        # 全てのイベントがprivateジャンルであることを確認
        assert len(events) >= 1
        for event in events:
            assert event["genre"] == "private"

    def test_filter_by_nonexistent_genre(self):
        """存在しないジャンルでフィルタした場合、空の配列が返ることを確認"""
        response = client.get("/api/events/?genre=nonexistent", headers=self.headers)
        assert response.status_code == 200
        events = response.json()
        assert len(events) == 0


class TestTask2UserTimestamp:
    """課題2: ユーザータイムスタンプ機能の検証"""

    def test_user_table_has_timestamp_fields(self):
        """usersテーブルにcreated_atとupdated_atフィールドが存在することを確認"""
        # SQLiteデータベースに直接接続してスキーマを確認
        conn = sqlite3.connect("calendar.db")
        cursor = conn.cursor()

        # テーブル情報を取得
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        conn.close()

        # created_at と updated_at が存在することを確認
        assert "created_at" in column_names
        assert "updated_at" in column_names

    def test_user_get_current_user_returns_created_at(self):
        """ユーザー情報取得時にcreated_atが返されることを確認"""
        headers = create_basic_auth_header("testuser", "testuser")
        response = client.get("/api/auth/me", headers=headers)

        assert response.status_code == 200
        user_data = response.json()

        # created_atフィールドが存在することを確認
        assert "created_at" in user_data

        # 現在時刻に近い値であることを確認（ISO形式の文字列として）
        created_at = user_data["created_at"]
        assert created_at is not None

        # ISO形式の日時文字列であることを確認
        try:
            datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail("created_at is not a valid ISO format datetime string")


class TestTask3ErrorMessageUnification:
    """課題3: APIエラーメッセージ統一の検証"""

    def test_invalid_start_date_format_error(self):
        """不正なstart_date形式のエラーメッセージが英語であることを確認"""
        headers = create_basic_auth_header("testuser", "testuser")
        response = client.get("/api/events/?start_date=invalid-date", headers=headers)
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid start_date format"

    def test_invalid_end_date_format_error(self):
        """不正なend_date形式のエラーメッセージが英語であることを確認"""
        headers = create_basic_auth_header("testuser", "testuser")
        response = client.get("/api/events/?end_date=invalid-date", headers=headers)
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid end_date format"

    def test_not_authenticated_error(self):
        """認証なしでアクセスした場合のエラーメッセージを確認"""
        response = client.get("/api/events/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"


class TestTask4EventOverlapCheck:
    """課題4: イベント重複チェック機能の検証"""

    def test_check_event_overlap_function_exists(self):
        """check_event_overlap関数が正しく実装されていることを確認"""
        try:
            from app.utils.validation import check_event_overlap
        except ImportError:
            pytest.fail("app.utils.validation.check_event_overlap function not found")

    def test_overlap_detection_with_existing_event(self):
        """既存イベントとの重複を正しく検出できることを確認"""
        from app.utils.validation import check_event_overlap
        
        # Basic認証でテスト用イベントを作成
        headers = create_basic_auth_header("testuser", "testuser")
        
        # 既存イベントを作成（10:00-12:00）
        event_data = {
            "title": "Existing Event",
            "description": "For overlap testing",
            "start": "2024-01-01T10:00:00",
            "end": "2024-01-01T12:00:00",
            "allDay": False,
            "genre": "work"
        }
        client.post("/api/events/", json=event_data, headers=headers)
        
        # ユーザーIDを取得
        user_response = client.get("/api/auth/me", headers=headers)
        user_id = user_response.json()["id"]

        # 重複するケース（11:00-13:00）
        result = check_event_overlap(
            user_id,
            datetime(2024, 1, 1, 11, 0),
            datetime(2024, 1, 1, 13, 0)
        )
        # 重複が検出されるはずなのでTrueが返される
        assert result is True

    def test_no_overlap_detection(self):
        """重複しない時間帯で正しくFalseを返すことを確認"""
        from app.utils.validation import check_event_overlap
        
        # Basic認証でユーザー情報を取得
        headers = create_basic_auth_header("testuser", "testuser")
        user_response = client.get("/api/auth/me", headers=headers)
        user_id = user_response.json()["id"]

        # 重複しないケース（15:00-16:00）
        result = check_event_overlap(
            user_id,
            datetime(2024, 1, 1, 15, 0),
            datetime(2024, 1, 1, 16, 0)
        )
        # 重複がないのでFalseが返される
        assert result is False
        
    def test_exclude_event_id_functionality(self):
        """exclude_event_idが正しく機能することを確認"""
        from app.utils.validation import check_event_overlap
        from app.database import SessionLocal
        from app.models.event import Event
        
        # Basic認証でテスト用イベントを作成
        headers = create_basic_auth_header("testuser", "testuser")
        
        # ユーザーIDを取得
        user_response = client.get("/api/auth/me", headers=headers)
        user_id = user_response.json()["id"]
        
        # テスト用の時間帯（他のテストと重複しないよう、より特殊な時間を使用）
        test_start = datetime(2024, 12, 25, 22, 30)  # 2024-12-25 22:30:00
        test_end = datetime(2024, 12, 25, 23, 30)    # 2024-12-25 23:30:00
        
        # 既存の同じ時間帯のイベントをクリーンアップ
        db = SessionLocal()
        try:
            db.query(Event).filter(
                Event.user_id == user_id,
                Event.start_datetime == test_start,
                Event.end_datetime == test_end
            ).delete()
            db.commit()
        finally:
            db.close()
        
        # 既存イベントを作成
        event_data = {
            "title": "Event for Exclusion Test",
            "description": "For testing exclude functionality",
            "start": test_start.isoformat(),
            "end": test_end.isoformat(),
            "allDay": False,
            "genre": "work"
        }
        create_response = client.post("/api/events/", json=event_data, headers=headers)
        assert create_response.status_code == 201
        created_event = create_response.json()

        # 同じ時間帯で重複チェック（exclude_event_idなし）
        result_without_exclude = check_event_overlap(
            user_id,
            test_start,
            test_end
        )
        # 重複が検出されるはずなのでTrueが返される
        assert result_without_exclude is True

        # 同じ時間帯で重複チェック（exclude_event_idあり）
        result_with_exclude = check_event_overlap(
            user_id,
            test_start,
            test_end,
            exclude_event_id=created_event["id"]
        )
        # 除外されるのでFalseが返される
        assert result_with_exclude is False
        
        # テスト後のクリーンアップ
        db = SessionLocal()
        try:
            db.query(Event).filter(Event.id == created_event["id"]).delete()
            db.commit()
        finally:
            db.close()


class TestTask5EventDurationCalculation:
    """課題5: イベント継続時間計算機能の検証"""

    def test_calculate_event_duration_function_exists(self):
        """calculate_event_duration_minutes関数が正しく実装されていることを確認"""
        try:
            from app.utils.datetime import calculate_event_duration_minutes
        except ImportError:
            pytest.fail("app.utils.datetime.calculate_event_duration_minutes function not found")

    def test_duration_calculation_accuracy(self):
        """継続時間が正しく計算されることを確認"""
        from app.utils.datetime import calculate_event_duration_minutes

        # 2時間30分のイベント
        duration = calculate_event_duration_minutes(
            datetime(2024, 1, 1, 10, 0),
            datetime(2024, 1, 1, 12, 30)
        )
        assert duration == 150

    def test_duration_in_api_response(self):
        """APIレスポンスにduration_minutesフィールドが含まれることを確認"""
        # Basic認証でアクセス
        headers = create_basic_auth_header("testuser", "testuser")

        # イベント作成
        event_data = {
            "title": "Duration Test Event",
            "description": "Testing duration",
            "start": "2024-01-01T10:00:00",
            "end": "2024-01-01T12:30:00",
            "allDay": False,
            "genre": "work"
        }
        client.post("/api/events/", json=event_data, headers=headers)

        # イベント一覧取得
        response = client.get("/api/events/", headers=headers)
        events = response.json()

        # duration_minutesフィールドの存在と値を確認
        assert len(events) > 0
        # 作成したイベントが含まれているかチェック
        duration_test_event = None
        for event in events:
            if event["title"] == "Duration Test Event":
                duration_test_event = event
                break
        
        assert duration_test_event is not None
        assert "duration_minutes" in duration_test_event
        assert isinstance(duration_test_event["duration_minutes"], int)
        assert duration_test_event["duration_minutes"] == 150


class TestTask6HealthCheck:
    """課題6: APIヘルスチェック機能の検証"""

    def test_health_endpoint_exists(self):
        """ヘルスチェックエンドポイントが存在することを確認"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_response_format(self):
        """ヘルスチェックのレスポンスフォーマットが正しいことを確認"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()

        # 必須フィールドの存在確認
        assert "status" in data
        assert "timestamp" in data

        # statusがhealthyまたはunhealthyであることを確認
        assert data["status"] in ["healthy", "unhealthy"]

        # timestampがISO形式であることを確認
        try:
            datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
        except ValueError:
            pytest.fail("timestamp is not a valid ISO format datetime string")

    def test_health_check_when_healthy(self):
        """正常時のヘルスチェックレスポンスを確認"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        # 通常の状態では healthy が返されるはず
        assert data["status"] == "healthy"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])