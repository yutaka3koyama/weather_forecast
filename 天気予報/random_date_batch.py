from datetime import datetime, timedelta
import random
from two_layer_net import TwoLayerNet

# 範囲日時の間のbatchサイズ分の日時を取り出す
def random_date_batch(start_date, end_date, batch_size) :
    s_date = datetime.strptime(start_date, "%Y-%m-%d")
    e_date = datetime.strptime(end_date, "%Y-%m-%d")
    e_date = e_date - timedelta(days = batch_size - 1)
    delta = e_date - s_date

    random_days = random.randint(0, delta.days)
    random_date = s_date + timedelta(days=random_days)
    random_date_plus_batch_size = random_date + timedelta(days = batch_size - 1)
    s_year = random_date.strftime('%y')
    s_month = random_date.strftime('%m')
    s_day = random_date.strftime('%d')
    e_year = random_date_plus_batch_size.strftime('%y')
    e_month = random_date_plus_batch_size.strftime('%m')
    e_day = random_date_plus_batch_size.strftime('%d')


    return 2000+int(s_year), int(s_month), int(s_day), 2000+int(e_year), int(e_month), int(e_day)
