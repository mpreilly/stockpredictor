from yahoo_finance import Share
import csv
from datetime import date
from datetime import timedelta

# Takes a stock, or multiple stocks, and formats it into a way that the data can
# be put into tensorflow. It only looks at prices. It looks at 5 consecutive
# days, then for the sixth day it assigns a classifier that tensorflow will use.
# Classifiers: 0 = decrease on sixth day, 1 = modest increase (0-3%),
# 2 = large increase (>3%)

# Learn on AMD, MU, BKS, with 1 year data
# Test on NVDA, SQ, MRVL with ~half year data
stocks = ['AMD', 'MU', 'BKS']
start_date = date(2016, 3, 3)
end_date = date.today()

def get_change(info, prevPrice):
    change = 100 * ((float(info.get('Close')) - float(prevPrice)) / float(prevPrice))
    return change

with open('training_data.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(('Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Class'))
    for stock in stocks:
        share = Share(stock)
        share.refresh()     # Refresh data from yahoo_finance
        history = share.get_historical(start_date.isoformat(), end_date.isoformat())

        count = 0
        changes = ()
        prevPrice = history.pop().get('Close')
        while len(history) > 5:
            info = history.pop()
            change = get_change(info, prevPrice)
            if count == 6:
                if change > 3:
                    changes += (2,) #classifier: 2 = large increase
                elif change > 0:
                    changes += (1,)
                else:
                    changes += (0,)
                count = 0
                writer.writerow(changes)
                changes = ()    #Set the row to empty again
                history.append(info)    #puts the info back so it's used as an actual data point
            else:
                changes += (change,)
                count += 1
                prevPrice = info.get("Close")
