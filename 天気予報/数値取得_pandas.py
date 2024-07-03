# 日付を知るためのモジュール
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# htmlを表にするためのモジュール
import pandas as pd
import numpy as np

# csvファイル保存で使うモジュール
import csv
import os

# サーバアクセスで待機時間を作るためのモジュール
import time

# データ取得開始と終了年月日を指定
start_year = 2023
start_month = 4
start_day = 14
end_year = 2024
end_month = 4
end_day = 13

# 指定の日付を取得
start_date = datetime(year=start_year, month=start_month, day=start_day, hour=0, minute=0, second=0, microsecond=0)
print('start_date =', start_date)
end_date = datetime(year=end_year, month=end_month, day=end_day, hour=0, minute=0, second=0, microsecond=0)
print('end_date =', end_date)

# start_dateとcurrent_dateの差分日数を取得
diff = end_date - start_date
diff_days = diff.days
print('diff_days =', diff_days)

# 観測地点を辞書型で指定 '地点名':[prec_no, block_no] 直接URL見て確認する
place = {'odawara' : [46, '1008'], 'ebina' : [46, '0388'], 'gotenba' : [50, '0441']}

# csvファイルをヘッダーをつけて作成

# 保存先のディレクトリとファイル名
directory = '/Users/yutaka3koyama/python/天気予報/神奈川県気象データ'
filename = 'weather_data.csv'

# ファイルパスを構築する
filepath = os.path.join(directory, filename)
print('filepath =', filepath)

# CSVファイルにデータを書き込む
with open(filepath, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['date', 'place', 'sun_dur', 'prec', 'weather_label', 'weather_no'])
    writer.writeheader()

# 第一ループ：日付を設定
for i in range(diff_days + 1) :

    print('i =', i)

    # 対象年月日の日付を出力
    date = start_date + relativedelta(days = i)
    print('date =', date)

    # 対象年月日の年/月/日をそれぞれ変数に代入
    year = date.strftime('%y')
    month = date.strftime('%m')
    day = date.strftime('%d')

    # 第二ループ：地点を設定
    for target_place in place :
        prec_no = place[target_place][0]
        block_no = place[target_place][1]

        # urlを指定
        url = f'https://www.data.jma.go.jp/obd/stats/etrn/view/hourly_a1.php?prec_no={prec_no}&block_no={block_no}&year=20{year}&month={month}&day={day}&view=p1'

        # urlのhtmlテーブルを参照してオブジェクト化
        dfs = pd.read_html(url)
        df = dfs[0] # 一つ目のテーブルを参照

        # 0-11時までのデータを取得

        # 日照時間とその合計値を算出
        sun_dur_row = df[('日照 時間 (h)', '日照 時間 (h)')][0:12]
        print('sun_dur_row =', sun_dur_row)
        if (sun_dur_row == '///').any() : # データに///(観測不可)が含まれる場合
            sun_dur_sum = False
            print('sun_dur_sum =', sun_dur_sum)
            sun_dur_rate = 'NULL'
        else :
            sun_dur_row = sun_dur_row.astype(float) # データにstrが混在した際floatにするため
            sun_dur_sum = np.nansum(sun_dur_row)
            print('sun_dur_sum =', sun_dur_sum)

            # 日照時間で数値の個数-1(補正)を取得
            valid_data_count = np.count_nonzero(~np.isnan(sun_dur_row[0:12])) - 1
            print('valid_date_count', valid_data_count)

            # 日照率を算出 
            sun_dur_rate = round(sun_dur_sum / valid_data_count, 3)
        print('sun_dur_rate =',sun_dur_rate)

        # 降水量合計を算出
        prec_row = df[( '降水量 (mm)',   '降水量 (mm)')][0:12]
        print('prec_row =', prec_row)
        if (prec_row == '///').any() : # データに///(観測不可)が含まれる場合
            prec_row_sum = 'NULL'
        else :
            prec_row = prec_row.astype(float) # データにstrが混在した際floatにするため
            prec_row_sum = sum(prec_row)
        print(f'降水量合計={prec_row_sum}')

        # 天気ラベルを設定
        # NULLの場合
        if sun_dur_rate == 'NULL' or prec_row_sum == 'NULL' :
            weather_label = 'NULL'
            weather_no = 'NULL'

        # 雲が有る場合
        elif sun_dur_rate <= 0.1 and prec_row_sum > 10 :
            weather_label = 'cyry' # cloud:yes, rain:yes
            weather_no = '1'
        elif sun_dur_rate <= 0.1 and prec_row_sum <= 10 and prec_row_sum > 0 :
            weather_label = 'cyrf' # cloud:yes, rain:few
            weather_no = '2'
        elif sun_dur_rate <= 0.1 and prec_row_sum == 0:
            weather_label = 'cyrn' # cloud:yes, rain:no
            weather_no = '3'

        # 雲が少し有る場合
        elif sun_dur_rate <= 0.9 and sun_dur_rate > 0.1 and prec_row_sum > 10 :
            weather_label = 'cfry' # cloud:few, rain:yes
            weather_no = '4'
        elif sun_dur_rate <= 0.9 and sun_dur_rate > 0.1 and prec_row_sum <= 10 and prec_row_sum > 0:
            weather_label = 'cfrf' # cloud:few, rain:few
            weather_no = '5'
        elif sun_dur_rate <= 0.9 and sun_dur_rate > 0.1 and prec_row_sum == 0 :
            weather_label = 'cfrn' # cloud:few, rain:no
            weather_no = '6'

        # 雲が無い場合
        elif sun_dur_rate > 0.9 and prec_row_sum > 10 :
            weather_label = 'cnry' # cloud:no, rain:yes
            weather_no = '7'
        elif sun_dur_rate > 0.9 and prec_row_sum <= 10 and prec_row_sum > 0 :
            weather_label = 'cnrf' # cloud:no, rain:few
            weather_no = '8'
        elif sun_dur_rate > 0.9 and sun_dur_rate > 0.1 and prec_row_sum == 0 :
            weather_label = 'cnrn' # cloud:no, rain:no
            weather_no = '9'

        # それ以外はERRORを返す
        else :
            weather_label = 'ERROR'
            weather_no = 'ERROR'

        # 日照率と降水量合計と天気ラベルを辞書変数へ代入
        date_join = int(str(year) + str(month) + str(day))
        new_row = {'date': date_join, 'place': target_place, 'sun_dur': sun_dur_rate, 'prec': prec_row_sum, 'weather_label': weather_label, 'weather_no': weather_no}

        with open(filepath, 'a', newline='') as file:
            # CSVライターオブジェクトを作成
            writer = csv.DictWriter(file, fieldnames=['date', 'place', 'sun_dur', 'prec', 'weather_label', 'weather_no'])

            # 新しい行をCSVファイルに書き込む
            writer.writerow(new_row)

        # DoS攻撃にならないためにスリープ
        time.sleep(2)


