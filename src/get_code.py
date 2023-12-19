import requests
from bs4 import BeautifulSoup
import pandas as pd


url = {
    'listed':'https://isin.twse.com.tw/isin/class_main.jsp?market=1&issuetype=1',
    'etf':'https://isin.twse.com.tw/isin/class_main.jsp?market=1&issuetype=I',
    'otc':'https://isin.twse.com.tw/isin/class_main.jsp?market=2&issuetype=4',
    'otc_etf':'https://isin.twse.com.tw/isin/class_main.jsp?market=2&issuetype=3'
}

code = []
for m in url:
    resp = requests.get(url[m])
    table = [tuple(map(lambda x: x.text, row.find_all('td'))) for row in BeautifulSoup(resp.text, "html.parser").find_all('tr')]
    code.append(pd.DataFrame(table[1:], columns=table[0]))
code = pd.concat(code, ignore_index=True)
code['有價證券代號'] = code['有價證券代號'].str.replace('\s', '')
code['key'] = ['.'.join([cd, 'tw' if mk == '上市 ' else 'two']) for cd, mk in code[['有價證券代號', '市場別']].values]
code.to_pickle('./data/code_tw.pkl')
