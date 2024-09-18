import requests
from datetime import datetime
import pytz

# OpenWeather APIキー
API_KEY = "15e07fd88434fffab3682ff0bbb36ba2"  # ここにAPIキーが書かれています

def get_weather_info(latitude, longitude):
    # OpenWeather APIのURL（f-stringの変数展開を修正）
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&lang=ja&units=metric"

    # APIから天気情報を取得
    response = requests.get(weather_url)
    
    try:
        weather_data = response.json()
    except json.JSONDecodeError:
        print("APIからの応答が正しいJSON形式ではありません")
        return
    
    if response.status_code != 200:
        print(f"エラーが発生しました: {weather_data.get('message', '不明なエラー')}")
        return

    # 天気情報の抽出
    weather_main = weather_data['weather'][0]['main']  # 天気（晴れ、雨など）
    weather_description = weather_data['weather'][0]['description']  # 詳細説明
    temperature = weather_data['main']['temp']  # 気温
    city_name = weather_data['name']  # 都市名

    # 日本時間での現在の時間を取得
    japan_time = datetime.now(pytz.timezone('Asia/Tokyo'))

    # 天気の表示
    print(f"場所: {city_name}")
    print(f"日本時間: {japan_time}")
    print(f"天気: {weather_description}")
    print(f"気温: {temperature}°C")

    # 傘が必要かの判断（例: 雨が含まれているかをチェック）
    if "雨" in weather_description:
        print("傘を用意してください")
    elif "晴" in weather_description:
        print("傘は必要ないでしょう")

if __name__ == "__main__":
    # 緯度と経度を直接コードに設定
    latitude = 35.0028724  # 例: 緯度
    longitude = 135.766041  # 例: 経度

    get_weather_info(latitude, longitude)