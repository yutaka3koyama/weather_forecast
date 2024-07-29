import os
import numpy as np
from PIL import Image
import pandas as pd
from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import glob
from gray_patch_std import get_std
import cv2
# from convert_label2binary import convert_label2binary

# 指定画像の画像データをnumpy配列で返す関数
def load_image(folder, filename) :
    pictures = glob.glob(os.path.join(folder, filename))
    img = cv2.imread(pictures[0], cv2.IMREAD_GRAYSCALE)
    new_size = (720, 960)
    resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR) # interpolationはサイズ変更時の計算方法
    img_array = get_std(resized_img)

    return img_array # numpy配列として返す

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
        return label
        # hot label方式で書いた場合
        # return convert_label2binary('all', label)
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

    # 訓練データ(データ100個の場合はe=7/21)
    train_images = load_specific_images('fujinomiya', s_year=2023, s_month=4, s_day=13, e_year=2023, e_month=5, e_day=13)
    train_labels = get_label('odawara', s_year=2023, s_month=4, s_day=14, e_year=2023, e_month=5, e_day=14)

    # テストデータ
    test_images = load_specific_images('fujinomiya', s_year=2024, s_month=3, s_day=1, e_year=2024, e_month=3, e_day=31)
    test_labels = get_label('odawara', s_year=2024, s_month=3, s_day=2, e_year=2024, e_month=4, e_day=1)

    # 訓練データを特徴量として使用(画像は3次元から1次元にする)
    X_train = np.array(train_images)
    y_train = np.array(train_labels)
    print('y train =', y_train)

    # テストデータを特徴量として使用(画像は3次元から1次元にする)
    X_test = np.array(test_images)
    y_test = np.array(test_labels)

    # 学習モデルの作成

    # # 非線形サポートベクターマシーン
    # model = SVC(C=0.3, kernel='rbf', random_state=0)

    # # k木近傍法
    # n_neighbors = int(np.sqrt(10))
    # model = KNeighborsClassifier(n_neighbors = n_neighbors)  

    # 線形サポートベクターマシーン
    model = LinearSVC(max_iter=1000, dual=False)

    model.fit(X_train, y_train)

    # テストデータで予測
    y_pred = model.predict(X_test)

    print(y_pred)
    print(y_test)

    # 精度を評価
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')
