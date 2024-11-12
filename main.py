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
macd_histogram = st.number_input("MACD Histogram:", step=0.0001, value=0.00017, format="%0.4f")
macd_line = st.number_input("MACD Line:", step=0.0001, format="%0.4f")
signal_line = st.number_input("Signal Line:", step=0.0001, format="%0.4f")

# RSI input
rsi = st.number_input("RSI value:", step=0.01, format="%0.2f")

st.subheader("Today's price")
px_open = st.number_input("Open")
px_high = st.number_input("High")
px_low = st.number_input("Low")
px_last = st.number_input("Last")

st.subheader("US Govt Bond Yield")
us_3ybond_col1, us_3ybond_col2 = st.columns(2)
three_y_yield = us_3ybond_col1.number_input("3y Yield", format="%0.2f")
three_y_yield_move = us_3ybond_col1.number_input("% Moved",  format="%0.2f", key="three_y_yield_move")

us_10ybond_col1, us_10ybond_col2 = st.columns(2)
ten_y_yield = us_10ybond_col1.number_input("10y Yield", format="%0.2f")
ten_y_yield_move = us_10ybond_col2.number_input("% Moved", format="%0.2f", key="ten_y_yield_move")

st.subheader("USD-AUD Exchange Rate")
fx_col1, fx_col2 = st.columns(2)
fx_usd_aud = fx_col1.number_input("USD-AUD",  format="%0.2f")
fx_usd_aud_move = fx_col2.number_input("% Moved",  format="%0.2f", key="fx_move")

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
                "content": """You are an expert in macroeconomic and bond market analysis. Use the following inputs on recent market data, technical indicators, and news to predict the likely direction for the Australian 3-year bond future (YM1) in the next trading session. The analysis should include a trading bias, bid range recommendations, and rationale. Additionally, highlight any upcoming economic events or data releases and explain the potential impact of varying outcomes on YM1.

                            1. **Recent Market News**: Analyze any significant economic or policy-related updates, including central bank actions, major economic indicators, or global economic news, especially from Australia, the U.S., or China. Identify any upcoming economic events or data mentioned in the news and provide possible outcomes and their implications for YM1.

                            2. **Today's pricing data and Technical indicators Analysis**: Analyze provided data to interpret current price momentum, trend strength, and possible price levels. Identify any oversold/overbought conditions or indications of reversal or continuation.

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

                Today's pricing data and Technical indicators for YM1 (3-Year Australian Bond Future) are as follows:
                - Datetime Now: {now_str}
                - Today's YM1 price in Open:{px_open}, High: {px_high}, Low: {px_low}, Last: {px_last}
                - Today's 3 Year U.S. Government Bond Yield:{three_y_yield}, moved {three_y_yield_move}% from yesterday
                - Today's 10 Year U.S. Government Bond Yield:{ten_y_yield}, moved {ten_y_yield_move}% from yesterday
                - Today's USD/AUD exchange rate: {fx_usd_aud}, moved {fx_usd_aud_move}% from yesterday
                - MACD Histogram: {macd_histogram}
                - MACD Line: {macd_line}
                - Signal Line: {signal_line}
                - RSI: {rsi}

                Request:
                Please analyze the impact of the upcoming news on YM1's direction, using the MACD, US government bond yield and USDAUD exchange rate data to provide insights on current momentum and price stability. Based on this analysis:
                1. Key Market Observations, summarize any major market movements, explain how changes can impact Australian 3-year bond future (YM1) in the next trading session. Highlight any recent economic or policy developments that might influence investor sentiment toward YM1.
                2. Technical Indicators Analysis. 
                3. Provide a trading bias for the next trading session, include a rationale.
                4. Suggest a primary bid range for the next trading session.
                5. Scenario Analysis for Upcoming Events: If the news highlights any upcoming economic event or data release, outline potential scenarios and their likely impact on YM1. For instance, discuss outcomes if inflation data exceeds expectations versus if it undershoots and describe the probable directional impact on YM1. Identify contingency bids for both upside and downside scenarios.
                6. Conclude with a short summary of the key analysis points, including the overall trading bias, recommended bid ranges, and any potential impacts from upcoming events.
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
