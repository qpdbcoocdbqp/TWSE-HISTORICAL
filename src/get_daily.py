import requests
import pandas as pd
import numpy as np
from datetime import datetime


resp = requests.get('https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL')
data = eval(resp.text)
res = pd.DataFrame(data['data'], columns=['ticker', 'name', 'volumn', 'turnover', 'open', 'high', 'low', 'close', 'spread', 'transaction'])
for int_type in ['volumn', 'turnover', 'transaction']:
    res[int_type] = res[int_type].str.replace(',', '').astype(np.int64)
for int_type in ['open', 'high', 'low', 'close']:
    res[int_type] = res[int_type].str.replace(',', '').astype(float)
res['spread'] = res['spread'].str.replace('(,|\+|X)', '').astype(float)
res['date'] = datetime.strptime(data['date'], '%Y%m%d')

past = pd.read_pickle('./data/stock_history.pkl')
pd.concat([res, past], ignore_index=True).to_pickle('./data/stock_history.pkl')
