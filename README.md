# FLUID-Pulse

**F.L.U.I.D. (Fast Learning Unified Intelligence Dynamics) Pulse** is an advanced automated quantitative stock screening engine designed for the Indian equity market (NSE). It combines momentum analysis, trend-following strategies, and AI-powered insights to identify high-probability breakout opportunities.

## Features

- **Quantitative Analysis**: Uses technical indicators (RSI, SMA) to filter stocks based on momentum and trend criteria
- **Intelligent Retry Logic**: Handles API rate limits gracefully with exponential backoff
- **AI-Generated Research**: Generates actionable market research reports for flagged opportunities
- **Real-time Data**: Fetches end-of-day (EOD) market data from Yahoo Finance
- **User-friendly Interface**: Built with Streamlit for easy interaction

## How It Works

1. Fetches 6-month historical data for top NSE stocks
2. Applies the F.L.U.I.D. quantitative filter (momentum + trend logic)
3. Flags stocks matching breakout criteria
4. Generates AI-powered research reports for each opportunity
