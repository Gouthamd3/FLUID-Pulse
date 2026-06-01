import os
from google import genai
from dotenv import load_dotenv  # 1. Import the dotenv loader

# 2. Load the variables from your local .env file
load_dotenv()

# 3. Initialize the Gemini Client securely
# This will look for GEMINI_API_KEY inside your .env file automatically.
# The hardcoded key fallback is completely removed so it never leaks on GitHub.
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
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
        # Calling the Gemini API
       response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
       return response.text.strip()
    
    except Exception as e:
        return f"Error generating content for {ticker}: {str(e)}"