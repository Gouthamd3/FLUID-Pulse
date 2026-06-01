#this file will contain code for a simple demonstration of FLUID technique of stock market data collection
import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
import requests

# Fetching data using yf
#by default 6mo period
def fetch_market_data(tickers, period="6mo"):
    # for fetching EOD data for list of tickers
    print("starting data collection")
    market_data = []

    for ticker in tickers:
        print(ticker)

        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    
        #Initialising the ticker object
        stock = yf.Ticker(ticker, session=session)

        #fetchig historical data
        df = stock.history(period=period)

        if not df.empty:
            df = df.reset_index()
            df = df[['Date', 'Open', 'High', 'Low','Close', 'Volume']]
            df['Ticker'] = ticker #Which stock this data belongs to
            
            market_data.append(df)
        else:
            print(f'Warning - No data found for {ticker}')
        
    #combining all individual stock df into one master df
    master_df = pd.concat(market_data, ignore_index=True)

    print("Data fetching complete \n")
    return master_df


