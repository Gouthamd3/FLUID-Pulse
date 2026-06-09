import streamlit as st
import time
from data_engine import fetch_market_data
from quant_filter import apply_fluid_filter
from ai_generator import generate_market_update

#UI Styling
st.set_page_config(page_title="F.L.U.I.D. Pulse", layout="centered")
st.title("F.L.U.I.D. Pulse Screener")
st.markdown("Automated Quantitative Breakout Engine & AI Content Generator")

st.markdown("""
**About F.L.U.I.D. Engine:**
F.L.U.I.D. (Fast Learning Unified Intelligence Dynamics) is an advanced quantitative stock screening engine that combines momentum analysis, trend-following strategies, and AI-powered insights to identify high-probability breakout opportunities in the Indian stock market. It uses technical indicators like RSI and SMA to filter stocks and generates actionable research reports.
""")

st.divider()

#run
if st.button("Run F.L.U.I.D. Engine", type="primary"):
    try:
        with st.spinner("Fetching EOD Market data..."):
            nse_tickers = [
                'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 
                'ITC.NS', 'SBIN.NS', 'TVSMOTOR.NS', 'DIXON.NS', 'HAL.NS', 'BHEL.NS'
            ]
            raw_market_data = fetch_market_data(nse_tickers, period="6mo")
    
    with st.spinner("Applying Momentum & Trend Logic..."):
        flagged_opportunities = apply_fluid_filter(raw_market_data)

    if not flagged_opportunities.empty:
        st.success(f"Discovered {len(flagged_opportunities)} momentum breakouts fitting the criteria.")

        #Displaying the math
        st.subheader("Quantitative Breakdown")
        st.dataframe(flagged_opportunities[['Ticker', 'Close', 'SMA_50', 'RSI_14']], hide_index=True)

        st.divider()
        st.subheader("AI-Generated Research Reports")
        
        # Generate and display the content
        for index, row in flagged_opportunities.iterrows():
            with st.spinner(f"Drafting report for {row['Ticker']}..."):
                report = generate_market_update(row['Ticker'], row['Close'], row['SMA_50'], row['RSI_14'])
                
                with st.expander(f"Market Update: {row['Ticker']}", expanded=True):
                    st.write(report)
            
            time.sleep(3)
    else:
        st.info("No stocks passed the strict F.L.U.I.D. momentum criteria today.")
    
    except Exception as e:
        st.error(f"⚠️ Rate Limit Error: Yahoo Finance API is rate-limited.")
        st.info("**What to do:**\n1. Wait 30-60 seconds\n2. Click the 'Run F.L.U.I.D. Engine' button again\n3. The app will automatically retry with intelligent backoff")
        st.caption(f"Error details: {str(e)[:100]}...")
