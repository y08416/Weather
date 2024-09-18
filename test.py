import requests
import json

# Supabaseの設定
SUPABASE_URL = "https://eeqflvnhxyfwqelztheu.supabase.co"
SUPABASE_API_KEY = "your-supabase-api-key"

# Lambda関数でSupabase API呼び出しを定義
add_item_to_supabase = lambda item_name: requests.post(
    f"{SUPABASE_URL}/rest/v1/item",
    headers={
        "Content-Type": "application/json",
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    },
    data=json.dumps({"name": item_name})
)

# Print statement with lambda for "傘を用意してください"
notify_to_prepare = lambda: print("傘を用意してください")

# 気象庁データの取得
jma_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
jma_json = requests.get(jma_url).json()

# 取得したいデータを選ぶ
jma_date = jma_json[0]["timeSeries"][0]["timeDefines"][0]
jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]

# 全角スペースの削除
jma_weather = jma_weather.replace('　', '')

# "雨"を検出したときの処理
if "雨" in jma_weather:
    response = add_item_to_supabase("傘")
    if response.status_code == 201:
        print("アイテム '傘'が追加されました")
    else:
        print(f"アイテムの追加に失敗しました: {response.status_code}, {response.text}")

    # 傘を用意する指示を出力
    notify_to_prepare()
elif "晴" in jma_weather:
    print("傘は必要ないでしょう")

print(jma_date)
print(jma_weather)