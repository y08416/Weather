import os
import requests
from dotenv import load_dotenv
from supabase import create_client, Client
import json
import firebase_admin
from firebase_admin import credentials, messaging

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPIキーとSupabaseの設定を取得
API_KEY = os.getenv("API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
firebase_credentials = json.loads(os.environ.get('FIREBASE_CREDENTIALS', '{}'))

# 環境変数の確認（デバッグ用）
print(f"API_KEY: {API_KEY}")
print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {SUPABASE_KEY}")
print(f"FCM_CREDENTIAL_PATH: {FCM_CREDENTIAL_PATH}")

# Firebase Admin SDK の初期化
if not firebase_admin._apps:
    cred = credentials.Certificate(FCM_CREDENTIAL_PATH)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK が正常に初期化されました。")

def get_weather_info(latitude, longitude):
    # OpenWeather APIのURL
    weather_url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"lat={latitude}&lon={longitude}&appid={API_KEY}&lang=ja&units=metric"
    )

    # APIから天気情報を取得
    response = requests.get(weather_url)

    try:
        weather_data = response.json()
    except json.JSONDecodeError:
        print("APIからの応答が正しいJSON形式ではありません")
        return None

    if response.status_code != 200:
        print(f"エラーが発生しました: {weather_data.get('message', '不明なエラー')}")
        return None

    # 天気情報の抽出
    weather_description = weather_data['weather'][0]['description']  # 詳細説明

    # 傘が必要かの判断（天気説明に「雨」が含まれているかどうか）
    if "雨" in weather_description:
        return "傘を用意してください"
    else:
        return "傘は必要ないでしょう"

def send_push_notification(user_id, message, fcm_token):
    if fcm_token:
        try:
            # 通知の構築
            notification = messaging.Notification(
                title="天気情報",
                body=message
            )
            message_data = messaging.Message(
                notification=notification,
                token=fcm_token
            )

            # 通知の送信
            response = messaging.send(message_data)
            print(f"User ID: {user_id} にプッシュ通知を送信しました。Response: {response}")

        except firebase_admin.exceptions.FirebaseError as e:
            print(f"User ID: {user_id} へのプッシュ通知の送信中にエラーが発生しました: {e}")
    else:
        print(f"User ID: {user_id} のfcm_tokenが登録されていません")

if __name__ == "__main__":
    # Supabaseクライアントの作成
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # 必要なカラムを一度に取得
    user_query = supabase.table("User").select("user_id,username,fcm_token").execute()

    if user_query.data:
        for user in user_query.data:
            user_id = user.get('user_id')
            fcm_token = user.get('fcm_token')
            print(fcm_token)

            if fcm_token:
                # Locationテーブルからlatitudeとlongitudeを取得
                location_query = supabase.table("Location").select("latitude", "longitude").eq("user_id", user_id).execute()

                if location_query.data:
                    location = location_query.data[0]
                    latitude = location.get('latitude')
                    longitude = location.get('longitude')
                    print(f"User ID: {user_id}, latitude={latitude}, longitude={longitude}")

                    weather_message = get_weather_info(latitude, longitude)
                    if weather_message:
                        send_push_notification(user_id, weather_message, fcm_token)
                else:
                    print(f"User ID: {user_id} の位置情報が見つかりませんでした")
            else:
                print(f"User ID: {user_id} のfcm_tokenが登録されていません")
    else:
        print("Userテーブルにデータが見つかりませんでした")