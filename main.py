import os
import requests
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

def get_uv_index(lat, lon, api_key):
    # 일반 날씨 API로 수정 (구독 불필요)
    # 일반 API는 UVI를 직접 제공하지 않으므로 UVI API를 호출해야 합니다.
    url = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={api_key}"
    
    print(f"DEBUG: [STARTED] get_uv_index")
    print(f"DEBUG: URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"DEBUG: Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"DEBUG: Error Response: {response.text}")
            raise Exception(f"API 호출 실패: {response.status_code}")
            
        data = response.json()
        print(f"DEBUG: API Response: {data}")
        
        # 일반 UVI API 응답 구조는 {'lat': ..., 'lon': ..., 'date': ..., 'value': ...}
        return data['value']
        
    except Exception as e:
        print(f"DEBUG: [EXCEPTION] {e}")
        raise e

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

    # 환경변수가 None인지 확인
    if not all([token, chat_id, api_key, lat, lon]):
        print("에러: 환경변수가 설정되지 않았습니다.")
        return

    try:
        uvi = get_uv_index(lat, lon, api_key)
        level = get_uv_level(uvi)

        message = f"☀️ 오늘 자외선 지수: {uvi} ({level})\n"
        if uvi >= 3:
            message += "자외선 지수가 높으니 선크림을 꼭 바르세요!"
        else:
            message += "오늘은 선크림을 바르지 않아도 됩니다."

        bot = Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message)
        print("메시지 전송 성공!")
    except Exception as e:
        print(f"실행 중 에러 발생: {e}")

if __name__ == "__main__":
    asyncio.run(main())
