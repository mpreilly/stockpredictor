from yahoo_finance import Share
from datetime import date
from datetime import timedelta
import numpy as np

# Calculate Simple Moving Average
def sma(symbol, numDays):
    share = Share(symbol)
    share.refresh()
    prices = []

    #Gather extra data to make sure we get enough for 20 days counting days off
    start_date = date.today() - timedelta(weeks=8)
    history = share.get_historical(start_date.isoformat(), date.today().isoformat())
    # Cut history list to get most recent 20 days
    history = history[:numDays]

    for info in history:
        prices.append(info['Close'])

    data = np.array(prices, dtype=np.float32)

    SMA = np.mean(data)
    return SMA

def ema(symbol, numDays, daysAgo=0):
    share = Share(symbol)
    share.refresh()
    prices = []

    start_date = date.today() - timedelta(weeks=60)
    history = share.get_historical(start_date.isoformat(), date.today().isoformat())
    history = history[:250]

    for i in range(1, numDays + 1):
        # starts with oldest data to calculate initial sma
        ind = -1 * i
        prices.append(history[ind]['Close'])

    data = np.array(prices, dtype=np.float32)
    SMA = np.mean(data)

    mult = 2.0 / (numDays + 1.0)
    EMA = SMA

    for i in range(numDays + 1, (len(history) + (1 - daysAgo))):
        ind = -1 * i
        EMA = (float(history[ind]['Close']) - EMA) * mult + EMA

    return EMA

def bollinger_bands(symbol):
    share = Share(symbol)
    share.refresh()
    prices = []

    #Gather extra data to make sure we get enough for 20 days counting days off
    start_date = date.today() - timedelta(weeks=8)
    history = share.get_historical(start_date.isoformat(), date.today().isoformat())
    # Cut history list to get most recent 20 days
    history = history[:20]

    for info in history:
        prices.append(info['Close'])

    data = np.array(prices, dtype=np.float32)

    # middle bollinger band: simple moving average
    SMA = np.mean(data)

    stdev = np.std(data)
    upper_band = SMA + 2 * stdev
    lower_band = SMA - 2 * stdev

    return SMA, upper_band, lower_band

def stochastic_oscillator(symbol):
    share = Share(symbol)
    share.refresh()

    # find high and low in last 14 days
    high = float(share.get_price())
    low = float(share.get_price())
    start_date = date.today() - timedelta(weeks=4)
    history = share.get_historical(start_date.isoformat(), date.today().isoformat())
    history = history[:14]

    for info in history:
        if float(info['High']) > high:
            high = float(info['High'])
        if float(info['Low']) < low:
            low = float(info['Low'])

    sto_osc = ((float(share.get_price()) - low) / (high - low)) * 100
    return sto_osc


# Calculates the Relative Strength Index by collecting 250 days of data,
# getting the average for the first 14 days and then updating it for each day to
# smooth it like it is done in the real world. Matches yahoo finance RSI.
def relative_strength_index(symbol):
    share = Share(symbol)
    share.refresh()

    start_date = date.today() - timedelta(weeks=60)
    history = share.get_historical(start_date.isoformat(), date.today().isoformat())
    history = history[:250]

    gain = 0
    loss = 0

    # first 14 days's averages
    for i in range(1, 15):
        # final - initial, with the dates in reverse chronological order
        ind = -1 * i
        change = float(history[ind - 1]['Close']) - float(history[ind]['Close'])

        if change >= 0:
            gain += change
        else:
            # we want loss to be positive. Subtract negative num gives us positive
            loss -= change

    avg_gain = gain / 14
    avg_loss = loss / 14

    # update the average for each of the rest of the days, ending at most recent
    for i in range(15, len(history)):
        gain = 0
        loss = 0

        ind = -1 * i
        change = float(history[ind - 1]['Close']) - float(history[ind]['Close'])

        if change >= 0:
            gain = change
        else:
            # we want loss to be positive. Subtract negative num gives us positive
            loss = -1 * change

        avg_gain = (avg_gain * 13 + gain) / 14
        avg_loss = (avg_loss * 13 + loss) / 14

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def macd(symbol):
    MACD = ema(symbol, 12) - ema(symbol, 26)

    total = 0
    # calculate 9-day average for signal line
    for i in range(1, 10):
        total += ema(symbol, 12, i) - ema(symbol, 26, i)

    signal = total / 9.0
    return MACD, signal
