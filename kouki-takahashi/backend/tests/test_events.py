from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """基本的なヘルスチェックテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint():
    """ルートエンドポイントの基本テスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
