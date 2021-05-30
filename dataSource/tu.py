import tushare as ts
import csv

ts.set_token('38d0a9576b98c8340d359c0ded6879b5aa4ab5011fb6fbe5b8cc001a')

pro = ts.pro_api()

date_list = ['20210430', '20210331', '20210226', '20210129', '20201231', '20201130', '20201030', '20200930', '20200831',
             '20200731', '20200630', '20200529', '20200430', '20200331', '20200228', '20200123', '20191231', '20191129',
             '20191031', '20190930', '20190830', '20190731', '20190628', '20190531']

# for i in date_list:
#     df = pro.monthly(trade_date=i, fields='ts_code,trade_date,change,pct_chg')
#     df.to_csv("./monthly/" + i + ".csv", index=False, sep=',')
#     if i != '20210430':
#         df.to_csv("./monthly/sum.csv", index=False, header=False, sep=',', mode='a+')
#     else:
#         df.to_csv("./monthly/sum.csv", index=False, sep=',', mode='a+')

stock_code = []
with open("./monthly/sum.csv", "r+") as file:
    for line in file:
        print(line[0:6])
        if line[0:6].isdigit() and line[0:6] not in stock_code:
            stock_code.append(line[0:6])
            with open("./stockData/" + line[0:6] + ".csv", 'w') as f:
                csv_write = csv.writer(f)
                head = ['stock_id', 'date', 'change', 'pct_chg']
                csv_write.writerow(head)
                new_line = [line[0:6], line[10:14] + "-" + line[14:16], line.split(',')[2], line.split(',')[3][0:-2]]
                csv_write.writerow(new_line)
            f.close()
        elif line[0:6].isdigit():
            with open("./stockData/" + line[0:6] + ".csv", 'a+') as f:
                new_line = [line[0:6], line[10:14] + "-" + line[14:16], line.split(',')[2], line.split(',')[3][0:-2]]
                csv_write = csv.writer(f)
                csv_write.writerow(new_line)
            f.close()

with open("./result/year.csv", 'w') as f0:
    csv_write = csv.writer(f0)
    head_year = ['stock_id', 'profit_possibility_year', 'avg_profit_year']
    csv_write.writerow(head_year)
f0.close()
with open("./result/half.csv", 'w') as f1:
    csv_write = csv.writer(f1)
    head_half = ['stock_id', 'profit_possibility_half', 'avg_profit_half']
    csv_write.writerow(head_half)
f1.close()
with open("./result/season.csv", 'w') as f2:
    csv_write = csv.writer(f2)
    head_season = ['stock_id', 'profit_possibility_season', 'avg_profit_season']
    csv_write.writerow(head_season)
f2.close()

# 盈利概率 平均盈利率
for n in range(len(stock_code)):
    with open("./stockData/" + stock_code[n] + ".csv", "r+") as file:
        print("./stockData/" + stock_code[n] + ".csv")
        reader = csv.reader(file)
        change = []
        pct = []
        for row in reader:
            change.append(row[2])
            pct.append(row[3])
        change = [float(x) for x in change[1:]]
        pct = [float(x) for x in pct[1:]]

        possibility_season = []
        average_income_season = []
        if len(change) < 3:
            with open("./result/season.csv", 'a+') as f:
                csv_write = csv.writer(f)
                csv_write.writerow(
                    [stock_code[n], '样本不足', '样本不足'])
            f.close()
        else:
            for i in range(len(change) - 2):
                if sum(change[i:i + 3]) > 0:
                    possibility_season.append(1)
                elif sum(change[i:i + 3]) < 0:
                    possibility_season.append(0)

                average_income_season.append(sum(pct[i:i + 3]))

            with open("./result/season.csv", 'a+') as f:
                csv_write = csv.writer(f)
                csv_write.writerow(
                    [stock_code[n],
                     sum(possibility_season) / len(possibility_season),
                     sum(average_income_season) / len(average_income_season)])
            f.close()

        possibility_half = []
        average_income_half = []
        if len(change) < 6:
            with open("./result/half.csv", 'a+') as f:
                csv_write = csv.writer(f)
                csv_write.writerow(
                    [stock_code[n], '样本不足', '样本不足'])
            f.close()
        else:
            for i in range(len(change) - 5):
                if sum(change[i:i + 6]) > 0:
                    possibility_half.append(1)
                elif sum(change[i:i + 6]) < 0:
                    possibility_half.append(0)

                average_income_half.append(sum(pct[i:i + 6]))

            with open("./result/half.csv", 'a+') as f:
                csv_write = csv.writer(f)
                csv_write.writerow(
                    [stock_code[n],
                     sum(possibility_half) / len(possibility_half),
                     sum(average_income_half) / len(average_income_half)])
            f.close()

        possibility_year = []
        average_income_year = []
        if len(change) < 12:
            with open("./result/year.csv", 'a+') as f:
                csv_write = csv.writer(f)
                csv_write.writerow(
                    [stock_code[n], '样本不足', '样本不足'])
            f.close()
        else:
            for i in range(len(change) - 11):
                if sum(change[i:i + 12]) > 0:
                    possibility_year.append(1)
                elif sum(change[i:i + 12]) < 0:
                    possibility_year.append(0)

                average_income_year.append(sum(pct[i:i + 12]))

            with open("./result/year.csv", 'a+') as f:
                csv_write = csv.writer(f)
                csv_write.writerow(
                    [stock_code[n],
                     sum(possibility_year) / len(possibility_year),
                     sum(average_income_year) / len(average_income_year)])
            f.close()
