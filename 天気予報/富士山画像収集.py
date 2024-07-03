# 画像ダウンロードに必要なライブラリ
import os
import requests

# 日の入り時刻を知るために使うライブラリ
import ephem

# 日付を知るために使うライブラリ
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# URLの画像を指定フォルダに指定ファイル名で保存するメソッドを定義
def save_image_from_url(url, filename, drct_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(drct_path, filename), 'wb') as f: # ws:'バイナリ'形式で'write'
            f.write(response.content)
            print(f"Image saved as {filename}")
    else:
        print("Failed to download image")

# 現在の日付のみを取得
current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

# 画像取得する最初の年月日=1年前の年月日を取得
start_date = current_date - relativedelta(years=1)

# start_dateとcurrent_dateの差分日数を取得
diff = current_date - start_date
diff_days = diff.days

# 静岡県富士市の緯度経度
shizuoka = ephem.Observer()
shizuoka.lat = '35.1613985'
shizuoka.lon = '138.6762728'

for i in range(diff_days) :

    print(f'i = {i}')

    # 対象年月日の日付を出す
    date = start_date + relativedelta(days = i)

    # 対象年月日の年/月/日をそれぞれ変数に入れる
    year = date.strftime('%y')
    month = date.strftime('%m')
    day = date.strftime('%d')

    # 指定したyear/month/dayの日の入り時刻を取得
    shizuoka.date = date
    sun = ephem.Sun()
    sunset_time = ephem.localtime(shizuoka.next_setting(sun, date))

    # 日の入り時刻の1時間前の'分'を四捨五入した'時'を取得
    if int(sunset_time.strftime('%M')) < 30 :
        hour_bfr = int(sunset_time.strftime('%H')) - 1
    else :
        hour_bfr = int(sunset_time.strftime('%H'))

    # 場所ごとの画像を取得
    for place in ('gotenba', 'fujinomiya', 'shimizu'):
        print(f'place= {place}')
        url = f'https://www.pref.shizuoka.jp/~live/archive/20{year}{month}{day}{place}/{hour_bfr}/xl.jpg'
        print(url)
        drct_path = f'/Users/yutaka3koyama/Pictures/富士山画像/{place}'
        filename = f"{year}{month}{day}{hour_bfr}{place}.jpg"
        save_image_from_url(url, filename, drct_path)
