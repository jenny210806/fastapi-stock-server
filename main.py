
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# CORS 설정 (iOS 앱에서 접근 가능하도록 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포시에는 앱 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 주식 항목 모델
class StockItem(BaseModel):
    symbol: str
    changePercent: float

# 추천 종목 응답 모델
class StockListResponse(BaseModel):
    stocks: List[StockItem]

# 추천 종목 API
@app.get("/recommend", response_model=StockListResponse)
def recommend_stocks():
    sample_stocks = [
        {"symbol": "AAPL", "changePercent": round(random.uniform(-5, 5), 2)},
        {"symbol": "GOOGL", "changePercent": round(random.uniform(-5, 5), 2)},
        {"symbol": "MSFT", "changePercent": round(random.uniform(-5, 5), 2)},
        {"symbol": "TSLA", "changePercent": round(random.uniform(-5, 5), 2)},
        {"symbol": "AMZN", "changePercent": round(random.uniform(-5, 5), 2)},
    ]
    return StockListResponse(stocks=[StockItem(**stock) for stock in sample_stocks])

# 상세 종목 API
@app.get("/detail/{stock_symbol}", response_model=StockItem)
def stock_detail(stock_symbol: str):
    return StockItem(
        symbol=stock_symbol,
        changePercent=round(random.uniform(-5, 5), 2)
    )
