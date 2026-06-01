# Import the functions from your other files
from data_engine import fetch_market_data
from quant_filter import apply_fluid_filter
from ai_generator import generate_market_update

def run_pipeline(export=False):
    print("Starting F.L.U.I.D. Pulse Engine...\n")
    
    #defining collection of stocks
    #.NS - for NSE stocks in yfinance

    # 1. Define the asset universe
    nse_tickers = [
        'RELIANCE.NS',  
        'TCS.NS',       
        'HDFCBANK.NS',  
        'ZOMATO.NS',    
        'INFY.NS',      
        'ITC.NS',
        'SBIN.NS',      # Corrected ticker
        'TVSMOTOR.NS',  # Added auto stock
        'DIXON.NS',     # High momentum electronics
        'HAL.NS',       # Defense sector momentum
        'BHEL.NS'
    ]

    # 2. Fetch the data (Calling function from data_engine.py)
    raw_market_data = fetch_market_data(nse_tickers, period="6mo")

    # 3. Apply the F.L.U.I.D. quant rules (Calling function from quant_filter.py)
    flagged_opportunities = apply_fluid_filter(raw_market_data)

    # 4. Display the results
    print("\n--- STOCKS PASSING THE SCREENER ---")
    if not flagged_opportunities.empty:
        print(flagged_opportunities[['Ticker', 'Close', 'SMA_50', 'RSI_14']])
        print("\n==================================================")
        print("GENERATING AI RESEARCH REPORTS VIA GEMINI AI...")
        print("==================================================\n")
    
        # Loop through each stock that passed the filter
        for index, row in flagged_opportunities.iterrows():
            ticker = row['Ticker']
            close = row['Close']
            sma_50 = row['SMA_50']
            rsi = row['RSI_14']
            
            print(f"--- F.L.U.I.D. Pulse Update: {ticker} ---")
            report = generate_market_update(ticker, close, sma_50, rsi)
            print(report)
            print("\n" + "-"*50 + "\n")
            
    else:
        print("No stocks passed the criteria today.")


    # For exporting data
    if export == True:
        # Find columns containing datetime objects with timezones
        tz_aware_cols = raw_market_data.select_dtypes(include=['datetime64[ns, UTC]', 'datetimetz']).columns
        # Convert them to naive
        raw_market_data[tz_aware_cols] = raw_market_data[tz_aware_cols].apply(lambda x: x.dt.tz_localize(None))
        raw_market_data.to_excel('output.xlsx', index=False)
        print("Data saved to output.xlsx")


# This ensures the script runs when you execute the file directly
if __name__ == "__main__":
    run_pipeline(export=False)  # Set to True if you want to export the data to Excel