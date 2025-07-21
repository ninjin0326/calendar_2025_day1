# バックエンド演習問題

以下の演習問題に沿ってソースコードを修正してください。どの問題から解いても構いません。

**注意**: 各問題を正確に採点するため、API仕様やエラーメッセージは**厳密に**指定通りに実装してください。<br>
./SUBMISSION.md ファイルの作成は不要です。

## 問題1. ジャンルフィルタ機能実装

### 課題

イベント一覧取得時にジャンルでフィルタする機能が不足している

### 要件

既存の`GET /api/events/`エンドポイントにクエリパラメータ`genre`を追加し、以下の出力を実現する：

**必須実装**:
- ジャンルによる完全一致フィルタ
- 大文字小文字の区別あり
- フィルタなしの場合は全件取得（既存動作維持）

**検証方法：APIレスポンス**
```bash
# 全件取得（既存動作維持）
curl -u testuser:testuser "http://localhost:8080/api/events/"
# → 全てのイベントが返される

# ジャンルフィルタ（work）
curl -u testuser:testuser "http://localhost:8080/api/events/?genre=work"
# → ジャンルが "work" のイベントのみが返される

# ジャンルフィルタ（private）
curl -u testuser:testuser "http://localhost:8080/api/events/?genre=private"
# → ジャンルが "private" のイベントのみが返される

# 存在しないジャンル
curl -u testuser:testuser "http://localhost:8080/api/events/?genre=nonexistent"
# → 存在しないジャンルであるため、どのイベントも返されない
```

**採点基準**:
- [ ] ジャンルフィルタが正常に動作する（完全一致）
- [ ] フィルタなしの場合も正常に動作する
- [ ] 存在しないジャンルで空配列が返される

### 見積

0.5時間

## 問題2. ユーザータイムスタンプ機能実装

### 課題

ユーザー管理でタイムスタンプが記録されていない

### 要件

ユーザーテーブルに以下のタイムスタンプフィールドを追加し、適切に設定されるようにする：

**必須実装**:
- `created_at`: ユーザー作成時刻（自動設定、ISO 8601形式）
- `updated_at`: ユーザー更新時刻（自動設定、ISO 8601形式）

**検証方法：データベーススキーマ**
```bash
# SQLiteスキーマ確認
sqlite3 calendar.db ".schema users"
# → created_at と updated_at フィールドが存在する

# 新規ユーザー作成時のタイムスタンプ確認
# 注: 現在の実装はBasic認証（username == password）のため、
# ユーザー登録エンドポイントは存在しません。
# ユーザー情報はget_current_userエンドポイントで確認できます。
curl -u testuser:testuser "http://localhost:8080/api/auth/me"
# → レスポンスにcreated_atが含まれ、ISO 8601形式で設定されている
```

**採点基準**:
- [ ] usersテーブルにcreated_atフィールドが存在する
- [ ] usersテーブルにupdated_atフィールドが存在する
- [ ] APIレスポンスにcreated_atが含まれる
- [ ] created_atがISO 8601形式である

### 見積

0.25時間

## 問題3. APIエラーメッセージ統一

### 課題

エラーレスポンスが日本語と英語で混在している

### 要件

以下の**特定のエラーケース**について、**完全に一致する**メッセージを返すように実装する：

**必須実装（厳密に以下のメッセージを返すこと）**:

| エラーケース | HTTPステータス | エラーメッセージ（exactMatch） |
|-------------|---------------|------------------------------|
| 不正なstart_date形式 | 400 | `Invalid start_date format` |
| 不正なend_date形式 | 400 | `Invalid end_date format` |
| Basic認証なし | 401 | `Not authenticated` |

**検証方法：エラーレスポンス**
```bash
# 不正な日付形式（認証必要）
curl -u testuser:testuser "http://localhost:8080/api/events/?start_date=invalid-date"
# → {"detail": "Invalid start_date format"}

curl -u testuser:testuser "http://localhost:8080/api/events/?end_date=invalid-date"
# → {"detail": "Invalid end_date format"}

# 認証なしの場合
curl "http://localhost:8080/api/events/"
# → {"detail": "Not authenticated"}
```

**採点基準**:
- [ ] 不正なstart_date形式で`Invalid start_date format`が返される
- [ ] 不正なend_date形式で`Invalid end_date format`が返される
- [ ] 認証なしで`Not authenticated`が返される
- [ ] HTTPステータスコードが正しい（400 or 401）

### 見積

0.5時間

## 問題4. イベント重複チェック機能実装

### 課題

同一ユーザーのイベントが時間重複してもエラーにならない

### 要件

`app/utils/validation.py`に重複チェック関数を実装し、イベント作成・更新時に使用する：

**必須実装**:
```python
def check_event_overlap(user_id: int, start_datetime: datetime, end_datetime: datetime, 
                       exclude_event_id: int = None) -> bool:
    """
    同一ユーザーのイベント時間重複をチェック
    
    Args:
        user_id: ユーザーID
        start_datetime: 開始日時
        end_datetime: 終了日時
        exclude_event_id: 除外するイベントID（更新時に使用）
    
    Returns:
        bool: 重複がある場合True、ない場合False
    """
```

**時間重複の定義**:
- 新イベントの開始時刻が既存イベントの期間内にある
- 新イベントの終了時刻が既存イベントの期間内にある
- 新イベントが既存イベントを完全に包含する
- 既存イベントが新イベントを完全に包含する

**検証方法：重複チェック関数**
```bash
# 仮想環境に入る
source venv/bin/activate

# イベントを作成
curl -X POST -u testuser:testuser -H "Content-Type: application/json" -d '{"title": "Existing Event",  "description": "For overlap testing", "start": "2024-01-01T10:00:00", "end": "2024-01-01T11:00:00", "allDay": false, "genre": "work"}' http://localhost:8080/api/events/

# 検証コマンド
python -c "
from app.utils.validation import check_event_overlap
from datetime import datetime
# 既存イベントと重複する場合のテスト
result = check_event_overlap(1, datetime(2024,1,1,10,0), datetime(2024,1,1,12,0))
print(f'Overlap result: {result}')  # → True

# 既存イベントと重複しない場合のテスト
result = check_event_overlap(1, datetime(2024,1,1,13,0), datetime(2024,1,1,14,0))
print(f'Overlap result: {result}')  # → False
"
```

**採点基準**:
- [ ] `app/utils/validation.py`に`check_event_overlap`関数が存在する
- [ ] 関数のシグネチャが正しい
- [ ] 既存イベントと重複する場合にTrueを返す
- [ ] 既存イベントと重複しない場合にFalseを返す
- [ ] exclude_event_idが正しく機能する

### 見積

0.75時間

## 問題5. イベント継続時間計算機能実装

### 課題

イベントの継続時間が計算されていない

### 要件

`app/utils/datetime.py`に継続時間計算関数を実装し、APIレスポンスに含める：

**必須実装**:
```python
def calculate_event_duration_minutes(start_datetime: datetime, end_datetime: datetime) -> int:
    """
    イベントの継続時間を分単位で計算
    
    Args:
        start_datetime: 開始日時
        end_datetime: 終了日時
    
    Returns:
        int: 継続時間（分）
    """
```

**検証方法：計算関数とAPIレスポンス**
```bash
# 仮想環境に入る
source venv/bin/activate

# 検証コマンド
python -c "
from app.utils.datetime import calculate_event_duration_minutes
from datetime import datetime
duration = calculate_event_duration_minutes(
    datetime(2024,1,1,10,0), 
    datetime(2024,1,1,12,30)
)
print(f'Duration: {duration} minutes')  # → 150
"

# APIレスポンスにduration_minutesフィールドが追加される
curl -u testuser:testuser "http://localhost:8080/api/events/"
# → "duration_minutes":60 が含まれる
```

### 補足

もし上記の検証コマンドでエラーが発生する場合は、一度データベースを初期化してください。
```bash
mv calendar.db calendar.db.bak  # 予定データを削除しバックアップ
# もし予定データが消えても良い場合は rm calendar.db
python -m app.init_db
```

**採点基準**:
- [ ] `app/utils/datetime.py`に`calculate_event_duration_minutes`関数が存在する
- [ ] 関数のシグネチャが正しい
- [ ] 継続時間の計算が正確
- [ ] APIレスポンスに`duration_minutes`フィールドが含まれる
- [ ] フィールドの値が整数型である

### 見積

0.5時間

## 問題6. APIヘルスチェック機能実装

### 課題

APIの稼働状況を確認する手段がない

### 要件

ヘルスチェックエンドポイント`GET /health`を実装し、以下の**厳密な**レスポンス形式を返す：

**必須実装場所**: `app/routes/health.py`を新規作成し、`app/main.py`でルーターを追加

**レスポンス形式（データベースに接続できる正常時）**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T10:00:00Z",
}
```

**レスポンス形式（データベースに接続できない異常時）**:
```json
{
  "status": "unhealthy",
  "timestamp": "2024-01-01T10:00:00Z",
}
```

**検証方法：ヘルスチェックAPI**
```bash
# ヘルスチェックエンドポイント
curl "http://localhost:8080/health"
# → {"status": "healthy", "timestamp": "2024-01-01T10:00:00Z"}

# データベース接続エラー時
curl "http://localhost:8080/health"
# → {"status": "unhealthy", "timestamp": "2024-01-01T10:00:00Z"}
```

**採点基準**:
- [ ] `/health`エンドポイントが存在する
- [ ] レスポンスに`status`フィールドが含まれる
- [ ] レスポンスに`timestamp`フィールドが含まれる（ISO 8601形式）
- [ ] 正常時に`status: "healthy"`が返される
- [ ] HTTPステータスコード200が返される

### 見積

0.5時間

**合計見積時間**: 約3時間

## 採点・提出について

### 自動テスト

適宜以下のテストを実行し、達成状況を確認してください。

```bash
# サーバーを起動した状態で別のターミナルを開き、backendディレクトリにある以下の採点スクリプトを実行する
# その後、全ての課題がpassすることを確認する（warningsへの対応は不要です）
sh ./scripts/test_all_features.sh
```

### 提出時の注意事項

1. **API仕様の遵守**: エラーメッセージやレスポンス形式は正確に実装する
2. **テストの実行**: 提出前に必ず自動テストを実行し、全てパスすることを確認する
3. **コードの可読性**: 適切な関数名・変数名・コメントを使用する
4. **ファイル配置**: 指定されたファイルパスに正確に実装する

### よくあるミス

- エラーメッセージの微細な差異（大文字小文字、句読点など）
- HTTPステータスコードの間違い
- レスポンスフィールド名の間違い
- 関数のシグネチャ（引数名・型）の間違い
- ファイルパスの間違い
