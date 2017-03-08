from yahoo_finance import Share
import csv

training_stocks = []
testing_stocks = []

with open('data/training_1day_data.csv','rb') as f:
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        if i != 0:
            training_stocks.append(row.pop(0))

with open('data/testing_1day_data.csv','rb') as f:
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        if i != 0:
            testing_stocks.append(row.pop(0))

print 'training stocks'
print training_stocks
print 'testing stocks'
print testing_stocks

with open('data/training_1day_nextdaychanges.csv','wb') as f:
    writer = csv.writer(f)
    for stock in training_stocks:
        share = Share(stock)
        share.refresh()
        writer.writerow((share.get_percent_change().replace("%","").replace("+",""),))

with open('data/testing_1day_nextdaychanges.csv','wb') as f:
    writer = csv.writer(f)
    for stock in testing_stocks:
        share = Share(stock)
        share.refresh()
        writer.writerow((share.get_percent_change().replace("%","").replace("+",""),))
