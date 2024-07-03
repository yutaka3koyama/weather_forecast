import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageOps

# csvファイル保存で使うモジュール
import csv
import os

# 画像データをnumpy配列で取得
pic_fujinomiya0 = cv2.imread('/Users/yutaka3koyama/Pictures/富士山画像/fujinomiya/23041317fujinomiya.jpg')
pic_gotenba0 = cv2.imread('/Users/yutaka3koyama/Pictures/富士山画像/gotenba/23041317gotenba.jpg')
pic_shimizu0 = cv2.imread('/Users/yutaka3koyama/Pictures/富士山画像/shimizu/23041317shimizu.jpg')

pic_fujinomiya = pic_fujinomiya0[0:670, 0:960]
pic_gotenba = pic_gotenba0[0:670, 0:960]
pic_shimizu = pic_shimizu0[0:670, 0:960]

bgr_array_3d = np.hstack((pic_fujinomiya, pic_gotenba, pic_shimizu))
print('array shape =', bgr_array_3d.shape)

# 2次元(1行)にしてDataFrameに変換
bgr_array_2d = bgr_array_3d.reshape(-1, bgr_array_3d.shape[2])
df = pd.DataFrame(bgr_array_2d, columns = ['B', 'G', 'R'])

# 保存先のディレクトリとファイル名
directory = '/Users/yutaka3koyama/python/天気予報/神奈川県気象データ'
filename = 'test1.csv'

# ファイルパスを構築する
filepath = os.path.join(directory, filename)

# CSVファイルにデータを書き込む
df.to_csv(filepath, index = False)
