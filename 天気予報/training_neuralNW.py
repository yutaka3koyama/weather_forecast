import os
import numpy as np
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import glob
import cv2
from convert_label2binary import convert_label2binary
from two_layer_net import TwoLayerNet
from random_date_batch import random_date_batch
import matplotlib.pyplot as plt

# 指定画像の画像データをnumpy配列で返す関数
def load_image(folder, filename) :
    pictures = glob.glob(os.path.join(folder, filename))
    # array = cv2.imread(pictures[0])
    img = cv2.imread(pictures[0], cv2.IMREAD_GRAYSCALE)
    new_size = (72, 96)
    resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR) # interpolationはサイズ変更時の計算方法
    array = np.array(resized_img)
    array = array.flatten()

    return array # numpy配列として返す

# 指定地点と範囲日付の画像データをリストで返す関数
def load_specific_images(place, s_year, s_month, s_day, e_year, e_month, e_day) :

    # 画像データのnumpy配列を入れるリストを用意
    images = []

    # フォルダーのパスを作成
    # 任意のディレクトリ中の指定placeフォルダ内に'富士山画像収集.py'で年月日がファイル名の画像を保存し参照
    folder = f'/Users/yutaka3koyama/Pictures/富士山画像/{place}'

    # 指定の日付を取得
    start_date = datetime(year=s_year, month=s_month, day=s_day, hour=0, minute=0, second=0, microsecond=0)
    print('start_date =', start_date)
    end_date = datetime(year=e_year, month=e_month, day=e_day, hour=0, minute=0, second=0, microsecond=0)
    print('end_date =', end_date)

    # start_dateとcurrent_dateの差分日数を取得
    diff = end_date - start_date
    diff_days = diff.days
    print('diff_days =', diff_days)

    # 対象日付の画像を読み込み
    for i in range(diff_days + 1) :

        # 対象年月日の日付を出力
        date = start_date + relativedelta(days = i)

        # 対象年月日の年/月/日をそれぞれ変数に代入
        year = date.strftime('%y')
        month = date.strftime('%m')
        day = date.strftime('%d')

        filename = f'{year}{month}{day}*.jpg'

        images.append(load_image(folder, filename))
    
    return images

# 地点と日付に合致するラベルデータを返す関数
def get_label_with_condition(date, place):

    # 任意のディレクトリ中に'数値取得_pandas.py'で'weather_data.csv'を作成し参照
    filepath_label = '/Users/yutaka3koyama/python/天気予報/神奈川県気象データ/weather_data.csv'
    df = pd.read_csv(filepath_label)

    # 条件に合致する行を取得
    row = df.loc[(df['date'] == date) & (df['place'] == place)]
    
    # 該当する行が存在する場合、その行のラベルの値を返す
    if not row.empty:
        label = row['weather_label'].values[0]
        # return label
        # hot label方式で書いた場合
        return convert_label2binary('all', label)
    else:
        return None

# 地点と日付範囲に合致するラベルデータをリストで返す変数
def get_label(place, s_year, s_month, s_day, e_year, e_month, e_day) :

    # ラベルを入れるリスト変数
    labels = []

    # 指定の日付を取得
    start_date = datetime(year=s_year, month=s_month, day=s_day, hour=0, minute=0, second=0, microsecond=0)
    print('start_date =', start_date)
    end_date = datetime(year=e_year, month=e_month, day=e_day, hour=0, minute=0, second=0, microsecond=0)
    print('end_date =', end_date)

    # start_dateとcurrent_dateの差分日数を取得
    diff = end_date - start_date
    diff_days = diff.days
    print('diff_days =', diff_days)

    # 対象日付のラベルを読み込み
    for i in range(diff_days + 1) :

        # 対象年月日の日付を出力
        date = start_date + relativedelta(days = i)

        # 対象年月日の年/月/日をそれぞれ変数に代入
        year = date.strftime('%y')
        month = date.strftime('%m')
        day = date.strftime('%d')
        simple_date = int(f'{year}{month}{day}')

        labels.append(get_label_with_condition(simple_date, place))
    
    return labels

## データ準備と学習モデル作成

if __name__ == '__main__' :

    network = TwoLayerNet(input_size=6912, hidden_size=100, output_size=9)

    iters_num = 5000  # 教科書のMNISTでは1エポックの1.5倍程度=500をデフォルト
    batch_size = 10
    train_size = 300 # 実際は365だがbatchで割り切れる数値に変更
    learning_rate = 0.5
    start_date = '2023-4-13'
    end_date = '2024-2-29'

    train_loss_list = []
    train_acc_list = []
    test_acc_list = []

    iter_per_epoch = max(train_size / batch_size, 1)

    # 1エポックごとに精度計算するためのテストデータを準備
    test_images = load_specific_images('gotenba', s_year=2024, s_month=3, s_day=1, e_year=2024, e_month=3, e_day=31)
    test_labels = get_label('gotenba', s_year=2024, s_month=3, s_day=2, e_year=2024, e_month=4, e_day=1)

    for i in range(iters_num):

        print('loop = ', i)

        # ランダムでbatch分の日付範囲を取得(画像用)
        s_year, s_month, s_day, e_year, e_month, e_day = random_date_batch(start_date, end_date, batch_size)

        # ランダムでbatch分の日付範囲を取得(ラベル用のため1日追加)
        label_s_date = datetime(year=s_year, month=s_month, day=s_day, hour=0, minute=0, second=0, microsecond=0)
        label_s_date = label_s_date + timedelta(days=1)
        s_year2 = 2000+int(label_s_date.strftime('%y'))
        s_month2 = int(label_s_date.strftime('%m'))
        s_day2 = int(label_s_date.strftime('%d'))

        label_e_date = datetime(year=e_year, month=e_month, day=e_day, hour=0, minute=0, second=0, microsecond=0)
        label_e_date = label_e_date + timedelta(days=1)
        e_year2 = 2000+int(label_e_date.strftime('%y'))
        e_month2 = int(label_e_date.strftime('%m'))
        e_day2 = int(label_e_date.strftime('%d'))

        # 訓練データ
        train_images = load_specific_images('fujinomiya', s_year, s_month, s_day, e_year, e_month, e_day)
        train_labels = get_label('odawara', s_year2, s_month2, s_day2, e_year2, e_month2, e_day2)

        # 勾配の計算
        # grad = network.numerical_gradient(np.array(train_images), np.array(train_labels))
        grad = network.gradient(np.array(train_images), np.array(train_labels))
        
        # パラメータの更新
        for key in ('W1', 'b1', 'W2', 'b2'):
            network.params[key] -= learning_rate * grad[key]
        
        loss = network.loss(np.array(train_images), np.array(train_labels))
        train_loss_list.append(loss)
        
        if i % iter_per_epoch == 0:
            train_acc = network.accuracy(np.array(train_images), np.array(train_labels))
            test_acc = network.accuracy(np.array(test_images), np.array(test_labels))
            train_acc_list.append(train_acc)
            test_acc_list.append(test_acc)
            print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))

    # グラフの描画
    markers = {'train': 'o', 'test': 's'}
    x = np.arange(len(train_acc_list))
    plt.plot(x, train_acc_list, label='train acc')
    plt.plot(x, test_acc_list, label='test acc', linestyle='--')
    plt.xlabel("epochs")
    plt.ylabel("accuracy")
    plt.ylim(0, 1.0)
    plt.legend(loc='lower right')
    plt.show()

