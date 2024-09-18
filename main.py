import requests
import json

# 気象庁データの取得
jma_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
jma_json = requests.get(jma_url).json()

# 取得したいデータを選ぶ
jma_date = jma_json[0]["timeSeries"][0]["timeDefines"][0]
jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]

# 全角スペースの削除
jma_weather = jma_weather.replace('　', '')

print(jma_date)
print(jma_weather)

# 「雨」と「晴」の条件分岐
if "雨" in jma_weather:
    print("傘を用意してください")
elif "晴" in jma_weather:
    print("傘は必要ないでしょう")