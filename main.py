import os
import re
import requests
from dotenv import load_dotenv
from supabase import create_client, Client
import json
import firebase_admin
from firebase_admin import credentials, messaging
import postgrest.exceptions

# .envファイルから環境変数を読み込む
API_KEY = "15e07fd88434fffab3682ff0bbb36ba2"
SUPABASE_URL = "https://eeqflvnhxyfwqelztheu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVlcWZsdm5oeHlmd3FlbHp0aGV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYxNDUyNzEsImV4cCI6MjA0MTcyMTI3MX0.k9cjeI55i9ajRCwbvJWxcNzLo2Pfy2VamkHXwRQdHss"

# Firebase認証情報をJSONとして直接指定
FCM_CREDENTIAL_PATH = {
  "type": "service_account",
  "project_id": "wasure-mobile",
  "private_key_id": "112937d51c86f3f773fa6dd309bb79d32a1cd3c3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCpFAnkK6ktW7Oy\nLavDVvlorMIABw2+YarzKe4UuATtDa98w1tDcLx8p0qg/CTapPY8RCvIdd0Ehd8D\nytDY422Wc+RrsgCm5uoyfkMkrJo9UFqqefEPEpZtApl28/LGwgiRYTY4UMgJMgnC\n5MBElzAvG/9uq4OsMX9bfjpNEUfOi0KO9VuveO358Xj/aP2SSPFncl2fWVy4sutZ\nYP8w/PB0Y9d2L11t9vRQdfOU2mt5+g5x1mhyMI8vaDXOaIfGC8Ul08G5QEGXBrFK\neEpn732ZlWmB8hJgGECS18qW2x9r0zxTNSG8ogRkJ725ch1x6TT95wzpn7aCGSUY\nRqGeYYwvAgMBAAECggEACMTgSnQ1PwP9iuUxfl0ZbGNhYGz9On2IRzpKfcqZfs3x\n5w+ewR2suO5YQYcyRiC+IJwMhUYPo3dp/KFdOZJ6EY6LL0a5H+7kAKBpzRIiocF0\nIllWtkhpgtfaq7+1PLe9iAS5siwGY+uzc+c3TZdlyVuzYMMGfjzG9TDTx0F5Lu4W\nahHMzdmGWgnCaKeppaI1/tVmhzgepEt9XdsDWSsqVW37i+0wh7fYndw5EMH0ARf8\n/egOVmQAZIAYMvl1TDxZXh0sjE9qFGUtwGX/GpYu7eQa8za8ctDm8tylX9yKtz7v\nIBirViY1b8zGzCeJLSkZ2Ax2KLsBhRN2YmRMPDJr6QKBgQDiec+3yKDB9Xd3UFqn\n8i7ptumHNrgeoBgSTt4shAdO+Cj/6shRaKPYauZCHQLtVe312c9/NkjrTO0tLRD8\n+Eb9rMGL5vG6dV3TEWYJ+9Lgu9NepwJUhPRk616BLgbe019SiU4RY5aP0bu4WiKa\nzsmXarijeKr/maoi6UI5yXS2ewKBgQC/HrIwnnDSpmXwVHH0hTl3APFGIaIU3exw\n2kevMB8q5IThMR5BzbaAUL+ZmCarBpliCP9vtxjDQPdAvFS8KLO2V10s5dEFhso4\n3Dmt9qwNKD5AOv0F0Ri6m639hxzQUKCfhki3ablRBaPJDJaVfTfxPXLIjRyc/jOM\noD3THsLM3QKBgQCAFdZlocFRkQtc3oQ3IeBoa/uNbmQZZf/XMuWylYUwo2dEvbtH\nV3/64RKS56eFJSks91/EGaaJ9XraJvfJqn0z8SWRgy7JfqFuwxNLqDGuymuTx66o\nsH0sKnXLZ4WZNkBeBKuzZ/h6JGsfq1KQ7UzUJxZ/1boYTwcLMZMz7XzlywKBgDhy\nPHaXlQLiGmFsz2tEncBECv6HmHNJSDfcgCeBsvLcI1LPSvxsYWZscupOQb1paYvG\n1IqOLUYdvejktrIL42gLTX2hMqbLNJaulGqI3C/Wnuwhf/Fj3EXhDPZAHYZ5CbeT\n1Y42L4F6hPEwQplMLmWVnH0XEEhd26PBAAGGqEoRAoGAStGGUYhMLvUjR5SBWnyh\neJLK9Bg5ujrhCfnvFZVQjY4WRHgIzEg+WRQm31tXbhU97pQYYO7BrtXzeRo4Edf+\nWQ0sgj8/ozPNCuY7wDRT2Rm5Kt+y269gBx/E5x90T+PUl7JSOOTz2XzwiDwPkMvf\nn+sC38Q76uoOh4u1SyL0nvM=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-htk3b@wasure-mobile.iam.gserviceaccount.com",
  "client_id": "113392731282029849176",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-htk3b%40wasure-mobile.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Firebase Admin SDK の初期化
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(FCM_CREDENTIAL_PATH)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK が正常に初期化されました。")
    except Exception as e:
        print("Firebase Admin SDK の初期化に失敗しました:", e)
        sys.exit(1)

# 環境変数の確認（デバッグ用）
print(f"API_KEY: {API_KEY}")
print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {SUPABASE_KEY}")
print(f"FCM_CREDENTIAL_PATH: {FCM_CREDENTIAL_PATH}")

# Firebase Admin SDK の初期化
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(FCM_CREDENTIAL_PATH)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK が正常に初期化されました。")
    except Exception as e:
        print("Firebase Admin SDK の初期化に失敗しました:", e)

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
            print(f"Processing User ID: {user_id}")
            print(f"FCM Token: {fcm_token}")

            # UUID形式の確認
            uuid_regex = re.compile(
                r'^[a-f0-9]{8}-[a-f0-9]{4}-[1-5][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}\Z', re.I)
            if not uuid_regex.match(user_id):
                print(f"Invalid user_id format: {user_id}")
                continue  # 不正な形式の場合はスキップ

            if fcm_token:
                try:
                    # Locationテーブルからlatitudeとlongitudeを取得
                    location_query = supabase.table("Location").select("latitude, longitude").eq("user_id", user_id).execute()
                except postgrest.exceptions.APIError as e:
                    print(f"Supabase APIError for user_id {user_id}: {e}")
                    continue
                except Exception as e:
                    print(f"Unexpected error for user_id {user_id}: {e}")
                    continue

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