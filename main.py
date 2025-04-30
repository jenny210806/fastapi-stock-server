
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 주식 항목 모델
class StockItem(BaseModel):
    symbol: str
    price: float
    changePercent: float
    volume: int

# 응답 모델
class StockListResponse(BaseModel):
    stocks: List[StockItem]

# 추천 종목 API
@app.get("/recommend", response_model=StockListResponse)
def recommend_stocks():
    sample_stocks = [
        {"symbol": "AAPL", "price": 185.12},
        {"symbol": "GOOGL", "price": 138.42},
        {"symbol": "MSFT", "price": 301.52},
        {"symbol": "TSLA", "price": 213.40},
        {"symbol": "AMZN", "price": 121.67},
        {"symbol": "NVDA", "price": 957.38},
        {"symbol": "META", "price": 491.12},
        {"symbol": "NFLX", "price": 612.77},
        {"symbol": "BABA", "price": 76.88},
        {"symbol": "INTC", "price": 31.45},
    ]

    stocks = [
        StockItem(
            symbol=stock["symbol"],
            price=stock["price"],
            changePercent=round(random.uniform(-5, 5), 2),
            volume=random.randint(100_000, 5_000_000)
        )
        for stock in sample_stocks
    ]

    return StockListResponse(stocks=stocks)

# 상세 종목 API
@app.get("/detail/{stock_symbol}", response_model=StockItem)
def stock_detail(stock_symbol: str):
    return StockItem(
        symbol=stock_symbol,
        price=round(random.uniform(50, 1000), 2),
        changePercent=round(random.uniform(-5, 5), 2),
        volume=random.randint(100_000, 5_000_000)        //마지막 수정: 테스트 주석
    )