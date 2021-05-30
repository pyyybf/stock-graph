import csv
import re
import json
import urllib.request
from sqlHelper import SqlHelper

stockgraph_sql = SqlHelper('../backend/sql/stockgraph.sql')
stockgraph_sql.write_init('StockGraph')
sample_sql = SqlHelper('../backend/sql/sample.sql')
sample_sql.write_init('StockGraph')

"""
写入Stock表
"""
stock_columns = {
    'id': ['int(11)', 'NOT NULL', 'AUTO_INCREMENT'],
    'name': ['varchar(255)', 'DEFAULT NULL'],
    'quarter_p': ['double', 'DEFAULT NULL'],
    'quarter_a': ['double', 'DEFAULT NULL'],
    'halfYear_p': ['double', 'DEFAULT NULL'],
    'halfYear_a': ['double', 'DEFAULT NULL'],
    'year_p': ['double', 'DEFAULT NULL'],
    'year_a': ['double', 'DEFAULT NULL'],
    'guarantee_a': ['double', 'DEFAULT NULL'],
}
stock_data = {}
sample_stock_data = {}
stock_list = []
print('============================获取股票列表============================')
with open('./resources/stock.csv', 'r', encoding='utf-8') as stock_csv:
    next(stock_csv)
    stock_csv_reader = csv.reader(stock_csv)
    for row in stock_csv_reader:
        stock_list.append(int(row[0]))
        stock_data[row[0]] = {
            'id': row[0],
            'name': row[1],
            'quarter_p': -2,
            'quarter_a': -2,
            'halfYear_p': -2,
            'halfYear_a': -2,
            'year_p': -2,
            'year_a': -2,
            'guarantee_a': 0
        }
        if int(row[0]) <= 100:
            sample_stock_data[row[0]] = {
                'id': row[0],
                'name': row[1],
                'quarter_p': -2,
                'quarter_a': -2,
                'halfYear_p': -2,
                'halfYear_a': -2,
                'year_p': -2,
                'year_a': -2,
                'guarantee_a': 0
            }
    stock_csv.close()

print('============================获取季度数据============================')
with open('./result/season.csv', 'r', encoding='utf-8') as season_csv:
    next(season_csv)
    season_csv_reader = csv.reader(season_csv)
    for row in season_csv_reader:
        if int(row[0]) in stock_list:
            stock_data[row[0]]['quarter_p'] = -2 if row[1] == '样本不足' else row[1]
            stock_data[row[0]]['quarter_a'] = -2 if row[2] == '样本不足' else row[2]
            if int(row[0]) <= 100:
                sample_stock_data[row[0]]['quarter_p'] = -2 if row[1] == '样本不足' else row[1]
                sample_stock_data[row[0]]['quarter_a'] = -2 if row[2] == '样本不足' else row[2]
    season_csv.close()

print('============================获取半年度数据============================')
with open('./result/half.csv', 'r', encoding='utf-8') as half_csv:
    next(half_csv)
    half_csv_reader = csv.reader(half_csv)
    for row in half_csv_reader:
        if int(row[0]) in stock_list:
            stock_data[row[0]]['halfYear_p'] = -2 if row[1] == '样本不足' else row[1]
            stock_data[row[0]]['halfYear_a'] = -2 if row[2] == '样本不足' else row[2]
            if int(row[0]) <= 100:
                sample_stock_data[row[0]]['halfYear_p'] = -2 if row[1] == '样本不足' else row[1]
                sample_stock_data[row[0]]['halfYear_a'] = -2 if row[2] == '样本不足' else row[2]
    half_csv.close()

print('============================获取年度数据============================')
with open('./result/year.csv', 'r', encoding='utf-8') as year_csv:
    next(year_csv)
    year_csv_reader = csv.reader(year_csv)
    for row in year_csv_reader:
        if int(row[0]) in stock_list:
            stock_data[row[0]]['year_p'] = -2 if row[1] == '样本不足' else row[1]
            stock_data[row[0]]['year_a'] = -2 if row[2] == '样本不足' else row[2]
            if int(row[0]) <= 100:
                sample_stock_data[row[0]]['year_p'] = -2 if row[1] == '样本不足' else row[1]
                sample_stock_data[row[0]]['year_a'] = -2 if row[2] == '样本不足' else row[2]
    year_csv.close()

print('============================计算担保总额============================')
# 获取汇率
url = "http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY&column=Code,Price"
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
req = urllib.request.Request(url)
f = urllib.request.urlopen(req)
html = f.read().decode("utf-8")
s = re.findall("{.*}", str(html))[0]
sjson = json.loads(s)
USDCNY = sjson["Data"][0][0][1] / 10000
print('当前汇率：{0}'.format(USDCNY))

non_decimal = re.compile(r'[^\d.]+')
with open('./resources/guarantee_pre.csv', 'r', encoding='utf-8') as guarantee_csv:
    next(guarantee_csv)
    guarantee_csv_reader = csv.reader(guarantee_csv)
    for row in guarantee_csv_reader:
        if int(row[2].split('-')[0]) < 2018:
            continue
        currency = 1
        if row[6] == '美元':
            currency = USDCNY
        if row[5][-1] == '亿':
            stock_data[row[0]]['guarantee_a'] += float(non_decimal.sub('', row[5])) * currency
        elif row[5][-1] == '万':
            stock_data[row[0]]['guarantee_a'] += float(non_decimal.sub('', row[5])) * currency * 0.0001
        if int(row[0]) <= 100:
            if row[5][-1] == '亿':
                sample_stock_data[row[0]]['guarantee_a'] += float(non_decimal.sub('', row[5])) * currency
            elif row[5][-1] == '万':
                sample_stock_data[row[0]]['guarantee_a'] += float(non_decimal.sub('', row[5])) * currency * 0.0001
    guarantee_csv.close()

stockgraph_sql.write_table('Stock', stock_columns, 'id', list(stock_data.values()))
sample_sql.write_table('Stock', stock_columns, 'id', list(sample_stock_data.values()))

"""
写入Event表
"""
event_columns = {
    'id': ['int(11)', 'NOT NULL', 'AUTO_INCREMENT'],
    'stock_id': ['int(11)', 'DEFAULT NULL'],
    'date': ['varchar(255)', 'DEFAULT NULL'],
    'type': ['varchar(255)', 'DEFAULT NULL'],
}
event_data = []
sample_event_data = []
with open('./resources/recent_pre.csv', 'r', encoding='utf-8') as recent_csv:
    next(recent_csv)
    recent_csv_reader = csv.reader(recent_csv)
    cur_id = 0
    for row in recent_csv_reader:
        if int(row[2].split('-')[0]) < 2018:
            continue
        cur_id += 1
        event_data.append({
            'id': cur_id,
            'stock_id': row[0],
            'date': row[2],
            'type': row[3]
        })
        if int(row[0]) <= 100:
            sample_event_data.append({
                'id': cur_id,
                'stock_id': row[0],
                'date': row[2],
                'type': row[3]
            })
    recent_csv.close()
stockgraph_sql.write_table('Event', event_columns, 'id', event_data)
sample_sql.write_table('Event', event_columns, 'id', sample_event_data)
