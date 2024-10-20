import openai
import streamlit as st
from scrape_news import TradingViewNewsScraper  # Import your TradingView scraper class
import time


# Streamlit app starts here
st.title("Auto YM for Cubs")

# Input to provide OpenAI API key file path
openai.api_key = st.text_input("Enter OpenAI API key:")

# Set the time window for news scraping
time_window = st.slider("Select Time Window for News Scraping (hours):", min_value=24, max_value=72, value=48)

# Initialize the scraper class
scraper = TradingViewNewsScraper(time_window=time_window)

news_items = None

# Button to fetch and display news
if st.button("Fetch and Analyze News"):
    with st.spinner("Fetching news and analyzing..."):
        # Fetch and scrape the news
        news_items = scraper.get_news()

        if not news_items:
            st.warning("No recent news articles found.")
        else:
            # Display scraped news
            st.subheader("Scraped News:")
            for i, news_item in enumerate(news_items):
                st.write(f"**{i+1}.** {news_item['content']}")
                st.write(f"**Source:** [Link]({news_item['url']})")
            
            # Compile the news into a single string for the OpenAI prompt
            compiled_news = "\n".join([f"{i+1}. {news_item['content']}" for i, news_item in enumerate(news_items)])
            
            # Define the macroeconomic expert role using a system message
            system_prompt = {
                "role": "system", 
                "content": "You are an expert in macroeconomic analysis with a focus on government bonds, \
                    interest rates, and market trends. You will read the news that is fed to you and analyze \
                    the impact of this news on the 3-year Australian government bond future (YM1) and provide \
                    your prediction for tomorrow's trading bias."
            }

            # Define today's news prompt with actual news content from TradingView
            user_prompt = {
                "role": "user", 
                "content": f"""
                Today's news about the Australian economy:
                {compiled_news}

                Analyze the impact of this news on the 3-year Australian government bond future (YM1) and provide your prediction for tomorrow's trading bias.
                Based on the news provided, what is the trading bias for tomorrow (bullish/bearish) and why?
                """
            }

            # Call OpenAI API
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",  # You can use gpt-4-turbo for cheaper and faster results
                    messages=[system_prompt, user_prompt],
                    temperature=0.5,  # Adjust this if you want more conservative or creative responses
                    max_tokens=500
                )
                
                # Parse and display the analysis
                macro_analysis = response['choices'][0]['message']['content']
                st.subheader("Macroeconomic Analysis:")
                st.write(macro_analysis)

            except Exception as e:
                st.error(f"Error in OpenAI API call: {e}")
# Input MACD (Histogram, MACD Line, Signal Line) and RSI values from the user
st.subheader("Technical Indicators Input")

# Current MACD values
st.write("### Current MACD")
macd_histogram = st.number_input("MACD Histogram:", step=0.0001, value=0.00017)
macd_line = st.number_input("MACD Line:", step=0.0001)
signal_line = st.number_input("Signal Line:", step=0.0001)

# RSI input
rsi = st.number_input("RSI value:", step=0.01)

# Button to analyze both news and technical indicators
if st.button("Analyze Trading Bias"):
    with st.spinner("Analyzing..."):
        # Compile the news into a single string for the OpenAI prompt (if available)
        if news_items:
            compiled_news = "\n".join([f"{i+1}. {news_item['content']}" for i, news_item in enumerate(news_items)])
        else:
            compiled_news = "No relevant news was found today."

        # Define the macroeconomic expert role using a system message
        system_prompt = {
            "role": "system", 
            "content": "You are an expert in macroeconomic and technical analysis. You will analyze \
                        the provided news, MACD, and RSI indicators to provide your prediction for tomorrow's trading bias."
        }

        # Define today's prompt including both news and technical indicators
        user_prompt = {
            "role": "user", 
            "content": f"""
            Today's news about the Australian economy:
            {compiled_news}

            The technical indicators for today are as follows:

            - MACD Histogram: {macd_histogram}%
            - MACD Line: {macd_line}%
            - Signal Line: {signal_line}%
            - RSI: {rsi}

            Based on the news and these technical indicators, analyze the impact on the 3-year Australian government bond future (YM1) and provide your prediction for tomorrow's trading bias. Explain whether it is bullish or bearish and why.
            """
        }

        # Call OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # You can use gpt-4-turbo for cheaper and faster results
                messages=[system_prompt, user_prompt],
                temperature=0.5,  # Adjust this if you want more conservative or creative responses
                max_tokens=500
            )
            
            # Parse and display the analysis
            macro_analysis = response['choices'][0]['message']['content']
            st.subheader("Trading Bias Prediction:")
            st.write(macro_analysis)

        except Exception as e:
            st.error(f"Error in OpenAI API call: {e}")