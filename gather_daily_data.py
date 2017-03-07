from yahoo_finance import Share
import os.path
import csv

stocks = ['AMD', 'MU', 'AAPL','NVDA','SNAP','SQ','ASX','GOOG','BLKB','CA','CSCO',
            'EA','FB', 'FIT','GRPN','HPQ','IBM','INTC','MRVL','MSFT','NOK','ORCL',
            'YHOO','ATVI']

for stock in stocks:
    path = 'data/' + stock + '.csv'
    if not os.path.isfile(path):
        with open(path, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(('Closing Price', 'Percent Change', 'Volume',
                            'PEG Ratio', 'Short Ratio', 'Pct Change From Year High',
                            'Pct Change From Year Low', 'Pct Change from 50 day mAvg',
                            'Ratio of price to 1 yr target price'))
    share = Share(stock)
    share.refresh()
    share.refresh()

    with open(path, 'a') as f:
        writer = csv.writer(f)

        row = (share.get_price(),
                share.get_percent_change(),
                share.get_volume(),
                share.get_price_earnings_growth_ratio(),
                share.get_short_ratio(),
                share.get_percent_change_from_year_high(),
                share.get_percent_change_from_year_low(),
                share.get_percent_change_from_50_day_moving_average())

        ratio_to_target = float(share.get_price()) / float(share.get_one_yr_target_price())
        row += (ratio_to_target,)
        writer.writerow(row)
