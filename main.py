from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pytrends.request import TrendReq

app = FastAPI()

# Разрешаем запросы с Tilda
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api/trends")
def get_trends(keyword: str):
    pytrends = TrendReq(hl="ru-RU", tz=180)
    pytrends.build_payload([keyword], timeframe="today 12-m", geo="RU")

    data = pytrends.interest_over_time()
    if data.empty:
        return {"error": "Нет данных"}

    trend_values = data[keyword].tolist()
    trend_dates = data.index.strftime("%Y-%m-%d").tolist()
    
    # Анализ динамики
    trend_change = (trend_values[-1] - trend_values[-4]) if len(trend_values) > 3 else 0
    recommendation = "📈 Рекомендуем увеличить бюджет!" if trend_change > 0 else "📉 Возможно, стоит снизить расходы."

    return {"dates": trend_dates, "values": trend_values, "recommendation": recommendation}
