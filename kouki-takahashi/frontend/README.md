# フロントエンド課題 - カレンダーアプリ

## 概要

React + TypeScript を使用したカレンダーアプリケーションのフロントエンド課題です。

## 技術スタック

- **フレームワーク**: React 18 + TypeScript
- **UI ライブラリ**: Material-UI (MUI)
- **カレンダー**: FullCalendar
- **ビルドツール**: Vite
- **日時処理**: Day.js
- **スタイリング**: Emotion + styled-components

## 必要な環境

- Node.js 20 以上
- npm

## セットアップと起動

### npm を使用

```bash
# フロントエンドディレクトリに移動
cd challenge/fßrontend

# 依存関係のインストール
npm install

# 開発サーバー起動（ポート3000）
npm run dev
```

### フロントエンドのみで開発する場合（モック API 使用）

```bash
# モックサーバーの起動（別ターミナル）
cd challenge/frontend/mock-server
npm install
npm start  # ポート3000で起動
```

`challenge/frontend/.env`ファイルの`VITE_BACKEND_URL`を 3001 に変更する

```bash
# フロントエンド開発サーバーの起動
cd challenge/frontend
npm run dev  # ポート3001で起動
```

## 動作確認

サーバー起動後、以下の URL でアプリケーションにアクセスできます：

- **アプリケーション**: http://localhost:3000

## バックエンド連携

このフロントエンドは`challenge/frontend/.env`で指定したバックエンド API と連携します。
バックエンド API と連携する処理は `src/features/api.ts` に記載されています。

### 認証情報

- **ユーザー名**: testuser
- **パスワード**: testuser

## 課題について

`TASK.md` の演習問題に沿ってソースコードを修正してください。どの問題から解いても構いません。

### 課題一覧

1. **分類ラベルの追加** (0.25 時間) - customer_visits、internal_meetings、external_meetings を追加
2. **UI レイアウト調整** (0.5 時間) - ヘッダーボタンの配置調整
3. **レスポンシブ対応** (0.5 時間) - 600px 以下での横スクロール対応
4. **バリデーション追加** (0.5 時間) - タイトル必須チェック
5. **日時表示形式の統一** (1 時間) - YYYY/MM/DD hh:mm 形式に統一
6. **削除機能の実装** (1 時間) - 削除ボタンと API 連携

**合計見積時間**: 約 3.25 時間

## 開発用コマンド

### ビルド

```bash
# プロダクション用ビルド
npm run build

# ビルド結果のプレビュー
npm run preview
```

### Lint・型チェック

```bash
# ESLintによるコード品質チェック
npm run lint

# TypeScriptの型チェック
tsc --noEmit
```

### テスト実行

```bash
# テストの実行
npm test

# テストをwatchモードで実行
npm test -- --watch

# テストのUIモードで実行
npm run test:ui

# テストカバレッジ付きで実行
npm test -- --coverage
```

### クリーンインストール

```bash
# node_modulesとpackage-lock.jsonを削除して再インストール
npm run install:clean
```

## ファイル構成

```
frontend/
├── src/
│   ├── App.tsx                    # メインアプリケーション
│   ├── main.tsx                   # エントリーポイント
│   ├── components/                # 共通コンポーネント
│   ├── features/                  # 機能別コンポーネント
│   │   ├── api.ts                # API通信
│   │   ├── const.ts              # 定数定義
│   │   ├── common/               # 共通機能
│   │   │   ├── calendar/         # カレンダー関連
│   │   │   └── events/           # イベント関連
│   │   └── routes/               # ページコンポーネント
│   ├── types/                     # TypeScript型定義
│   └── utils/                     # ユーティリティ
├── mock-server/                   # モックAPI サーバー
├── public/                        # 静的ファイル
├── package.json                   # 依存関係・スクリプト
├── vite.config.ts                # Vite設定
├── tsconfig.json                 # TypeScript設定
└── README.md                     # このファイル
```

## トラブルシューティング

### API 連携エラーの場合

1. バックエンドサーバーが起動しているか確認
2. 認証情報が正しいか確認

### パッケージエラーの場合

```bash
# Node.jsのバージョンが20以上であることを確認
node --version

# npmキャッシュのクリア
npm cache clean --force

# 依存関係の再インストール
rm -rf node_modules package-lock.json
npm install
```
