# バックエンド課題 - FastAPI カレンダーAPI

## 概要

FastAPI + SQLAlchemy を使用したカレンダーアプリケーションのバックエンドAPI課題です。

## 技術スタック

- **フレームワーク**: FastAPI
- **データベース**: SQLite + SQLAlchemy
- **認証**: Basic認証
- **バリデーション**: Pydantic
- **ASGIサーバー**: Uvicorn

## 必要な環境

- **Python**: 3.13以上
- **pip**: Python パッケージ管理ツール

## セットアップと起動

### 仮想環境の使用

```bash
# バックエンドディレクトリに移動
cd solution/backend

# 仮想環境の作成
python3.13 -m venv venv

# 仮想環境の有効化
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# email-validatorのインストール
pip install "pydantic[email]"

# データベースの初期化
python3.13 -m app.init_db

# サーバー起動（ポート8080）
python3.13 -m app.main
```

## 動作確認

サーバー起動後、以下のURLで動作確認できます：

- **API ドキュメント（Swagger UI）**: http://localhost:8080/docs
- **API ドキュメント（ReDoc）**: http://localhost:8080/redoc
- **ヘルスチェック**: http://localhost:8080/health

## フロントエンドとの連携

このバックエンドは以下のフロントエンドと連携します：

- **フロントエンドURL**: http://localhost:3000
- **CORS設定**: フロントエンドからのリクエストを許可

## 課題について

`TASK.md` の演習問題に沿ってソースコードを修正してください。どの問題から解いても構いません。

### 課題一覧

1. **API仕様追加** (0.5時間) - ジャンルフィルタ機能の実装
2. **データベース設計改善** (0.25時間) - ユーザーテーブルの作成日時追加
3. **エラーハンドリング改善** (0.5時間) - エラーメッセージの統一
4. **バリデーション追加** (0.75時間) - タイトルバリデーションの実装
5. **レスポンス形式改善** (0.5時間) - 作成・更新時のレスポンス統一
6. **APIドキュメント改善** (0.5時間) - docstringの充実

**合計見積時間**: 約3時間

## API エンドポイント

### 認証

- `POST /api/auth/login` - ログイン

### イベント

- `GET /api/events` - イベント一覧取得
- `POST /api/events` - イベント作成
- `GET /api/events/{id}` - 特定イベント取得
- `PUT /api/events/{id}` - イベント更新
- `DELETE /api/events/{id}` - イベント削除

### ユーザー

- `GET /api/users` - ユーザー一覧取得

## 開発用コマンド

### テスト実行

```bash
# テストの実行
pytest

# より詳細な出力でテスト実行
pytest -v

# カバレッジ付きテスト
pytest --cov=app tests/

# HTMLレポート付きカバレッジ
pytest --cov=app --cov-report=html tests/

# 特定のテストファイルのみ実行
pytest tests/test_events.py

# 特定のテスト関数のみ実行
pytest tests/test_events.py::test_health_check

# failfast（最初のエラーで停止）
pytest -x

# 並列実行（pytest-xdistが必要）
pytest -n auto
```

### データベースリセット

```bash
# データベースファイルを削除して再初期化
rm calendar.db
python3.13 -m app.init_db
```

## トラブルシューティング

### パッケージエラーの場合

```bash
# 依存関係を最新版に更新
pip install -r requirements.txt --upgrade

# email-validatorのインストール
pip install "pydantic[email]"
```

## ファイル構成

```
backend/
├── app/
│   ├── main.py              # FastAPIアプリケーション
│   ├── database.py          # データベース設定
│   ├── init_db.py          # データベース初期化
│   ├── models/             # SQLAlchemyモデル
│   │   ├── user.py
│   │   └── event.py
│   ├── routes/             # APIルート
│   │   ├── auth.py
│   │   ├── events.py
│   │   └── users.py
│   ├── schemas/            # Pydanticスキーマ
│   │   ├── user.py
│   │   └── event.py
│   └── utils/              # ユーティリティ
│       └── security.py
├── tests/                   # テストファイル
├── requirements.txt         # 依存関係
├── calendar.db             # SQLiteデータベース（自動生成）
└── README.md               # このファイル
```

## 開発のヒント

### APIテスト方法

```bash
# ヘルスチェック
curl http://localhost:8080/health

# イベント一覧取得（認証付き）
curl -u testuser:testuser http://localhost:8080/api/events/

# 新規イベント作成
curl -X POST -u testuser:testuser \
  -H "Content-Type: application/json" \
  -d '{"title":"新規会議","start_datetime":"2025-07-08T14:00:00","end_datetime":"2025-07-08T15:00:00","genre":"work","all_day":false}' \
  http://localhost:8080/api/events/
```

### よくあるエラーと解決方法

1. **Python 3.13 + SQLAlchemy互換性エラー**
   ```bash
   # requirements.txtで適切なバージョンを指定済み
   pip install -r requirements.txt
   ```

2. **email-validator関連エラー**
   ```bash
   pip install "pydantic[email]"
   ```

3. **ポート使用中エラー**
   ```bash
   # 別のポートで起動
   PORT=8081 python -m app.main
   ```
