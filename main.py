import os
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPIキーとSupabaseの設定を取得
API_KEY = os.getenv("API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_weather_info(latitude, longitude):
    # OpenWeather APIのURL
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
    weather_description = weather_data['weather'][0]['description']  # 詳細説明

    # 傘が必要かの判断（天気説明に「雨」が含まれているかどうか）
    if "雨" in weather_description:
        print("傘を用意してください")
    else:
        print("傘は必要ないでしょう")

if __name__ == "__main__":
    # Supabaseクライアントの作成
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Userテーブルからuser_idを取得
    user_query = supabase.table("User").select("user_id").execute()

    if user_query.data:
        for user in user_query.data:
            user_id = user['user_id']
            
            # Locationテーブルからlatitudeとlongitudeを取得
            location_query = supabase.table("Location").select("latitude, longitude").eq("user_id", user_id).execute()
            
            if location_query.data:
                location = location_query.data[0]
                latitude = location['latitude']
                longitude = location['longitude']
                print(f"User ID: {user_id}, latitude={latitude}, longitude={longitude}")
                get_weather_info(latitude, longitude)
            else:
                print(f"User ID: {user_id} の位置情報が見つかりませんでした")
    else:
        print("Userテーブルにデータが見つかりませんでした")