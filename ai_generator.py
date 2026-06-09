import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# 1. Load local .env variables if running locally
load_dotenv()


def get_gemini_api_key():
    """Return GEMINI_API_KEY from Streamlit secrets or environment variables."""
    api_key = None

    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Missing GEMINI_API_KEY. Set it in Streamlit secrets or as an environment variable."
        )

    return api_key


def get_genai_client():
    return genai.Client(api_key=get_gemini_api_key())


def generate_market_update(ticker, close, sma_50, rsi):
    #use stock's metrics and generate expert analysis using this together ai

    prompt = f"""
    You are an expert in SEBI-registered analyst's automated assistant at Reco Wealth.
    Write a concise, high-quality, 2-paragraph market update for a premium investor community based on these exact quantitative metrics:
    - Stock Ticker: {ticker}
    - Current Closing Price: ₹{close:.2f}
    - 50-day Simple Moving Average (SMA): ₹{sma_50:.2f}
    - 14-day Relative Strength Index (RSI): {rsi:.2f}

    Guidelines:
    1. Paragraph 1 should focus on the technical trend, noting that the price is trading strongly above its 50-day SMA, indicating robust structural momentum.
    2. Paragraph 2 should interpret the RSI, explaining that the momentum is healthy and not yet in extreme overbought territory, making it a text-book momentum breakout candidate fitting our F.L.U.I.D. criteria.
    3. Keep the tone professional, highly objective, and completely free of conversational AI filler text. Do not include introductory text like "Here is your summary". Start directly with the content.
    """

    try:
        client = get_genai_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip()
    
    except Exception as e:
        return f"Error generating content for {ticker}: {str(e)}"
