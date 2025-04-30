from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests

# 인증 토큰 (Bearer)과 계좌정보 등은 보안을 위해 환경변수 또는 설정 파일로 관리하는 것을 권장합니다.
KIS_BASE_URL = "https://openapi.koreainvestment.com:9443"
ACCESS_TOKEN = "여PSU3zd44SR6uT1jVAgSII0JzLyc29ForoGwIuv"

HEADERS = {
    "Content-Type": "application/json",
    "authorization": f"Bearer {ACCESS_TOKEN}",
    "appkey": "PSU3zd44SR6uT1jVAgSII0JzLyc29ForoGwIY",
    "appsecret": "mkK34AxvbDtY7gfuRfVS81C0Xj2KAW4ouue9nHGM7wdxeXXwINJ8FaDAqo05sOT7apyDKkU5jfHn26MY1ByMhCnaFyAEGUJUS2JBuRFB1hYhdP+fr7Vh8Oyki5Oj42lnDrIs12j9G86YEITjtkEkEMnqCHmvz0vtSf+0VW8SkXVd7RuO3ws=",
    "tr_id": "FHKST01010100",  # 국내 주식 시세 조회용 TR
}

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

# 종목 리스트 (예: 국내 주식 코드)
STOCK_CODES = [
    ("005930", "삼성전자"),
    ("000660", "SK하이닉스"),
    ("035420", "NAVER"),
    ("207940", "삼성바이오로직스"),
    ("035720", "카카오"),
    ("051910", "LG화학"),
    ("068270", "셀트리온"),
    ("096770", "SK이노베이션"),
    ("066570", "LG전자"),
    ("105560", "KB금융")
]

@app.get("/recommend", response_model=StockListResponse)
def recommend_stocks():
    result = []

    for code, name in STOCK_CODES:
        url = f"{KIS_BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-price?fid_cond_mrkt_div_code=J&fid_input_iscd={code}"

        try:
            res = requests.get(url, headers=HEADERS)
            data = res.json()["output"]

            price = float(data["stck_prpr"])
            change = float(data["prdy_vrss_sign"]) * float(data["prdy_ctrt"])
            volume = int(data["acml_vol"])

            result.append(StockItem(
                symbol=name,
                price=price,
                changePercent=change,
                volume=volume
            ))

        except Exception as e:
            print(f"Error fetching {name}: {e}")

    return StockListResponse(stocks=result)

@app.get("/detail/{stock_symbol}", response_model=StockItem)
def stock_detail(stock_symbol: str):
    # 종목명을 코드로 변환
    matched = [code for code, name in STOCK_CODES if name == stock_symbol]
    if not matched:
        return {"error": "종목을 찾을 수 없습니다."}

    code = matched[0]
    url = f"{KIS_BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-price?fid_cond_mrkt_div_code=J&fid_input_iscd={code}"

    res = requests.get(url, headers=HEADERS)
    data = res.json()["output"]

    price = float(data["stck_prpr"])
    change = float(data["prdy_vrss_sign"]) * float(data["prdy_ctrt"])
    volume = int(data["acml_vol"])

    return StockItem(
        symbol=stock_symbol,
        price=price,
        changePercent=change,
        volume=volume
    )