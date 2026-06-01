import numpy as np

#default 14 periods
#SMA or EMA for rsi calc
#using ema will result in less accuracy, as t-1 day's avergae price is not available easily, so we can ue sma's average for this
def calculate_rsi(data, window=14, method='SMA'):
    #calc of rsi

    delta = data['Close'].diff() #price change
    #SMA
    if method == 'SMA':
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    #EMA
    if method == 'EMA':
        gain = (delta.where(delta > 0, 0)).ewm(span=window, adjust=False).mean()
        loss = (-delta.where(delta < 0, 0)).ewm(span=window, adjust=False).mean()

    # Avoid division by zero
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100/ (1+rs))

    return rsi.fillna(0)

def apply_fluid_filter(df):
    #momentum & trend rules to market data
    #group by tickers

    print("Applying F.L.U.I.D. Quant Rules...")

    #sort data chronologically
    df = df.sort_values(by=['Ticker', 'Date'])

    #indicator calc for every ticker
    df['SMA_50'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=50).mean())
    df['SMA_200'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=200).mean())
    df['RSI_14'] = df.groupby('Ticker').apply(lambda x: calculate_rsi(x)).reset_index(level=0, drop=True)

    #most recent data for screening
    latest_data = df.groupby('Ticker').last().reset_index()

    #screener-fluid rules
    """
    1. Price is above the 50 day SMA - short term momentum
    2. 50 day SMA is above 200 day SMA - Long term uptrend or golden cross
    3. RSI is between 55 and 75 (momentum is strong - not overbought)
    """

    #filtering data by applying the rules to the df
    screened_stocks = latest_data[
        (latest_data['Close'] > latest_data['SMA_50']) &
        (latest_data['RSI_14'] > 50) &
        (latest_data['RSI_14'] < 80)
    ]

    return screened_stocks
