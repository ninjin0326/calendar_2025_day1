from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from app.database import create_tables
from app.routes import events, users, auth

# 環境変数の読み込み
load_dotenv()

app = FastAPI(
    title="Calendar API",
    description="フルスタックWebエンジニアインターン課題 - カレンダーアプリAPI",
    version="1.0.0",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
    allow_headers=["Origin", "Content-Length", "Content-Type", "Authorization"],
    max_age=43200,  # 12時間
)

# データベーステーブル作成
create_tables()

# ルート登録
app.include_router(auth.router, prefix="/api/auth", tags=["認証"])
app.include_router(events.router, prefix="/api/events", tags=["イベント"])
app.include_router(users.router, prefix="/api/users", tags=["ユーザー"])


@app.get("/")
async def root():
    return JSONResponse(
        content={"message": "Calendar API Server", "docs": "/docs", "redoc": "/redoc"}
    )


@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),  # フロントエンドと競合しないポート
        reload=True,
    )
