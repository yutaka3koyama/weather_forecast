import cv2
import numpy as np

# 指定ピクセルの周辺3x3のピクセルの輝度値の平均を計算する関数
def calc_avg_brt(image, center, size=9):
    x, y = center
    half_size = size // 2

    # 画像の境界を超えないように領域を制限
    start_x = max(0, x - half_size)
    end_x = min(image.shape[0], x + half_size + 1)
    start_y = max(0, y - half_size)
    end_y = min(image.shape[1], y + half_size + 1)

    # 指定された領域のピクセルを抽出
    patch = image[start_x:end_x, start_y:end_y]

    # 平均輝度を計算
    average_brightness = np.mean(patch)
    return average_brightness

# 各座標の周辺ピクセルの列ごとの標準偏差を出力
def get_std(fuji) :
    
    coordinates = [
        (180, 240), (360, 240), (540, 240),
        (180, 480), (360, 480), (540, 480),
        (180, 720), (360, 720), (540, 720)
    ]
    # coordinates = [
    #     (18, 24), (36, 24), (54, 24),
    #     (18, 48), (36, 48), (54, 48),
    #     (18, 72), (36, 72), (54, 72)
    # ]

    avg_list = []
    for coord in coordinates :
        avg_list.append(calc_avg_brt(fuji, coord))
    patch_avg = [avg_list[i:i+3] for i in range(0, len(avg_list), 3)]

    # 標準偏差を計算して出力
    patch_std = []
    for i in range(len(patch_avg)) :
        patch_std.append(np.std(patch_avg[i]))
    return patch_std

if __name__ == '__main__' :
    # 画像の読み込み
    fuji1 = cv2.imread('/Users/yutaka3koyama/Pictures/富士山画像/fujinomiya/23110716fujinomi*.jpg', cv2.IMREAD_GRAYSCALE)
    new_size = (72, 96)
    fuji = cv2.resize(fuji1, new_size, interpolation=cv2.INTER_LINEAR) # interpolationはサイズ変更時の計算方法


    print('fuji shape =', fuji.shape)
    cv2.imshow('sample', fuji)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(get_std(fuji))