import os
import requests
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

def get_uv_index(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url).json()
    # OpenWeatherMap One Call 3.0 returns uvi in current object
    return response['current']['uvi']

def get_uv_level(uvi):
    if uvi < 3:
        return "낮음"
    elif uvi < 6:
        return "보통"
    elif uvi < 8:
        return "높음"
    elif uvi < 11:
        return "매우 높음"
    else:
        return "위험"

async def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    api_key = os.getenv('OPENWEATHER_API_KEY')
    lat = os.getenv('LATITUDE')
    lon = os.getenv('LONGITUDE')

    uvi = get_uv_index(lat, lon, api_key)
    level = get_uv_level(uvi)

    message = f"☀️ 오늘 자외선 지수: {uvi} ({level})\n"
    if uvi >= 3:
        message += "자외선 지수가 높으니 선크림을 꼭 바르세요!"
    else:
        message += "오늘은 선크림을 바르지 않아도 됩니다."

    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    asyncio.run(main())
