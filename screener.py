import indicators as ind
import data_collection as dc
from yahoo_finance import Share

stocks, _ = dc.get_random_stocks(1000,0)
for stock in stocks:
    print stock
    sma, top, bot = ind.bollinger_bands(stock)

    print sma, top, bot
    #skips stocks that couldn't get the data
    if sma == 0:
        continue

    share = Share(stock)
    price = share.get_price()

    # prints the stocks that have price below bottom bollinger band and MACD
    # if float(price) < bot:
    #     print stock

    MACD, signal = ind.macd(stock)

    print "\tMACD: %d, signal: %d, price: %d, bot bol: %d" % (MACD, signal, price, bot)
    if MACD > signal and (float(price) - bot < (float(price) * .03)):
        print "*********", stock
