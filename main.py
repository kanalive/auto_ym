import openai
import streamlit as st
from scrape_news import TradingViewNewsScraper  # Import your TradingView scraper class
import time
import datetime

# Streamlit app starts here
st.title("Auto YM for Cubs")

# Input to provide OpenAI API key
openai.api_key = st.text_input("Enter OpenAI API key:")

# Set the time window for news scraping
time_window = st.slider("Select Time Window for News Scraping (hours):", min_value=0, max_value=72, value=24)

# Initialize the scraper class
scraper = TradingViewNewsScraper(symbol="TVC:AU03Y", time_window=time_window)

audusd_news_scraper = TradingViewNewsScraper(symbol="FX%3AAUDUSD", time_window=time_window)

usd_bond_scraper = TradingViewNewsScraper(symbol="CBOT%3AZB1!", time_window=time_window)

us_inflation_scraper = TradingViewNewsScraper(symbol="ECONOMICS%3AUSIRYY", time_window=time_window)


# Input MACD (Histogram, MACD Line, Signal Line) and RSI values from the user
st.subheader("Technical Indicators Input")

# Current MACD values
macd_histogram = st.number_input("MACD Histogram:", step=0.0001, value=0.00017)
macd_line = st.number_input("MACD Line:", step=0.0001)
signal_line = st.number_input("Signal Line:", step=0.0001)

# RSI input
rsi = st.number_input("RSI value:", step=0.01)

st.subheader("Today's price")
px_open = st.number_input("Open")
px_high = st.number_input("High")
px_low = st.number_input("Low")
px_last = st.number_input("Last")

now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

total_news_items = []

# Button to analyze news and technical indicators together
if st.button("Fetch News and Analyze Trading Bias"):
    with st.spinner("Fetching news and analyzing..."):
        try:
            # Fetch and scrape the news
            news_items = scraper.get_news()

            usd_aud_news_items = audusd_news_scraper.get_news()

            usd_bond_news_items = usd_bond_scraper.get_news()

            us_inflation_news_items = us_inflation_scraper.get_news()

            total_news_items = news_items + usd_aud_news_items + usd_bond_news_items + us_inflation_news_items

            # Compile the news into a single string for the OpenAI prompt (if available)
            if total_news_items:
                compiled_news = "\n".join([f"{i+1}. {news_item['content']}" for i, news_item in enumerate(news_items)])
            else:
                compiled_news = "No relevant news was found today."

            # Define the macroeconomic expert role using a system message
            system_prompt = {
                "role": "system", 
                "content": """You are an advanced market analyst specializing in interpreting economic news, technical indicators, and recent market movements to provide actionable trading insights. For each request, analyze the upcoming economic events, relevant market indicators, and price trends to develop a comprehensive bid strategy.

                            1. **Economic and Market Developments**: Evaluate the potential impact of upcoming economic events or recent news on the asset (e.g., YM1). Explain how the news might influence market sentiment, yields, or other key economic variables.

                            2. **Technical Indicator Analysis**: Analyze provided MACD and RSI data to interpret current price momentum, trend strength, and possible price levels. Identify any oversold/overbought conditions or indications of reversal or continuation.

                            3. **Trading Bias and Scenario Analysis**: Based on the economic context and technical analysis, outline possible bullish or bearish scenarios. Assess how each scenario would influence the trading bias for the asset (bullish, bearish, or neutral).

                            4. **Suggested Bid Strategy**:
                            - Identify a primary bid range for the next trading session based on the analysis.
                            - Include contingent bids for both upside and downside scenarios, explaining how each bid level aligns with the market's potential reaction to economic events or technical levels.

                            Structure the response in a clear format, labeling each section for easy reference.
                            """
            }

            # Define today's prompt including both news and technical indicators
            user_prompt = {
                "role": "user",
                "content": f"""
                Please analyze today's news regarding the Australian 3-Year Government Bond Yield, USD/AUD, and U.S. Treasury Bond Futures:

                News Summary:
                {compiled_news}

                Technical indicators for YM1 (3-Year Australian Bond Future) are as follows:
                - Datetime Now: {now_str}
                - Today's YM1 price in Open:{px_open}, High: {px_high}, Low: {px_low}, Last: {px_last}
                - MACD Histogram: {macd_histogram}
                - MACD Line: {macd_line}
                - Signal Line: {signal_line}
                - RSI: {rsi}

                Request:
                Please analyze the impact of the upcoming news on YM1's direction, using the MACD and RSI data to provide insights on current momentum and price stability. Based on this analysis:
                1. Describe the potential outcomes based on varying scenarios of the fiscal package (e.g., strong, moderate, minimal support).
                2. Provide a trading bias for each scenario.
                3. Suggest a primary bid range for the next trading session and identify contingency bids for both upside and downside scenarios.
                4. Include a rationale for each bid range to help refine trading strategy.

                """
            }

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # You can use gpt-4-turbo for cheaper and faster results
                messages=[system_prompt, user_prompt],
                temperature=0.4,  # Adjust this if you want more conservative or creative responses
                max_tokens=16384
            )

            # Parse and display the analysis
            macro_analysis = response['choices'][0]['message']['content']
            st.subheader("Trading Bias Prediction:")
            st.write(macro_analysis)

            st.divider()
            st.write(total_news_items)
                

        except Exception as e:
            st.error(f"Error in OpenAI API call: {e}")
