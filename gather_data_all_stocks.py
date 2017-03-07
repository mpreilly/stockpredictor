from yahoo_finance import Share
import csv
import random

all_companies = []
training_stocks = []
testing_stocks = []


with open('data/companylist.csv','rb') as f:
    reader = csv.reader(f)
    for row in reader:
        all_companies.append(row.pop(0))

for i in range(0,500):
    training_stocks.append(all_companies.pop(random.randint(1, len(all_companies)-1)))

print training_stocks


#Create training csv
with open("data/training_1day_data.csv", 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(('Closing Price', 'Percent Change', 'Volume',
                        'PEG Ratio', 'Short Ratio', 'Pct Change From Year High',
                        'Pct Change From Year Low', 'Pct Change from 50 day mAvg',
                        'Ratio of price to 1 yr target price'))

    for i in range(0,500):
        stock = training_stocks[i]
        share = Share(stock)
        share.refresh()
        share.refresh() #sometimes yahoo doesn't refresh correctly

        # Replace this stock with another if it doesn't have a target price or target price is 0
        while share.get_one_yr_target_price() is None or float(share.get_one_yr_target_price()) == 0:
            training_stocks.pop(i)
            stock = all_companies.pop(random.randint(1, len(all_companies)-1))
            training_stocks.insert(i, stock)
            share = Share(stock)

        row = (share.get_price(),
                share.get_percent_change().replace("%","").replace("+",""),
                share.get_volume(),
                share.get_price_earnings_growth_ratio(),
                share.get_short_ratio(),
                share.get_percent_change_from_year_high().replace("%","").replace("+",""),
                share.get_percent_change_from_year_low().replace("%","").replace("+",""),
                share.get_percent_change_from_50_day_moving_average().replace("%","").replace("+",""))


        ratio_to_target = float(share.get_price()) / float(share.get_one_yr_target_price())
        row += (ratio_to_target,)

        writer.writerow(row)
        print('%d: %s') % (i+1, stock) #show progress
print training_stocks



for i in range(0,100):
    testing_stocks.append(all_companies.pop(random.randint(1, len(all_companies)-1)))

with open("data/testing_1day_data.csv", 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(('Closing Price', 'Percent Change', 'Volume',
                        'PEG Ratio', 'Short Ratio', 'Pct Change From Year High',
                        'Pct Change From Year Low', 'Pct Change from 50 day mAvg',
                        'Ratio of price to 1 yr target price'))
    for i in range(0,100):
        stock = testing_stocks[i]
        share = Share(stock)
        share.refresh()
        share.refresh() #sometimes yahoo doesn't refresh correctly

        # Replace this stock with another if it doesn't have a target price or target price is 0
        while share.get_one_yr_target_price() is None or float(share.get_one_yr_target_price()) == 0:
            testing_stocks.pop(i)
            stock = all_companies.pop(random.randint(1, len(all_companies)-1))
            testing_stocks.insert(i, stock)
            share = Share(stock)

        row = (share.get_price(),
                share.get_percent_change().replace("%","").replace("+",""),
                share.get_volume(),
                share.get_price_earnings_growth_ratio(),
                share.get_short_ratio(),
                share.get_percent_change_from_year_high().replace("%","").replace("+",""),
                share.get_percent_change_from_year_low().replace("%","").replace("+",""),
                share.get_percent_change_from_50_day_moving_average().replace("%","").replace("+",""))

        # put in the ratio of current price to 1 yr target price
        ratio_to_target = float(share.get_price()) / float(share.get_one_yr_target_price())
        row += (ratio_to_target,)

        writer.writerow(row)
        print('%d: %s') % (i+1, stock) #show progress
print testing_stocks
