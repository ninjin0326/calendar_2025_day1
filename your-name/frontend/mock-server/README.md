# カレンダーアプリ モックAPIサーバー

このディレクトリには、フロントエンド開発用のモックAPIサーバーが含まれています。

## セットアップ

```bash
cd frontend/mock-server
npm install
```

## 起動方法

### 認証あり（推奨）
```bash
npm start
```

### 認証なし（テスト用）
```bash
npm run start:no-auth
```

## API エンドポイント

### イベント管理
- `GET /api/events` - イベント一覧取得
- `POST /api/events` - イベント作成
- `GET /api/events/:id` - 特定イベント取得
- `PUT /api/events/:id` - イベント更新
- `DELETE /api/events/:id` - イベント削除

### ユーザー管理
- `GET /api/users` - ユーザー一覧取得
- `GET /api/users/:id` - 特定ユーザー取得

## 認証

Basic認証を使用します：
- ユーザー名: 任意の文字列
- パスワード: 任意の文字列

ユーザー名とパスワードは、`challenge/frontend/.env`の環境変数`VITE_USERNAME`,`VITE_PASSWORD`の値が使用されます。

## データ構造

### Event
```json
{
  "id": "string",
  "title": "string", 
  "start": "ISO 8601 datetime string",
  "end": "ISO 8601 datetime string",
  "genre": "work" | "private" | "other",
  "allDay": boolean,
  "users": ["string"]
}
```

### User
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "created_at": "ISO 8601 datetime string"
}
```

## フロントエンドとの連携

フロントエンドを起動する前に、`challenge/frontend/.env`の環境変数を設定してください。

例：
```bash
VITE_BACKEND_URL=http://localhost:3001
VITE_USERNAME=testuser
VITE_PASSWORD=testuser
```