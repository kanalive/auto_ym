# Auto YM1

This project is a **Streamlit-based web app** that scrapes macroeconomic news about Australian government bonds and feeds it into OpenAI's GPT-4o model for analysis. The app helps to predict the trading bias for Australian 3-year bond futures (YM1) based on the latest news.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

---

## Introduction

This project was built for **learning** and **sharing** purposes, designed to demonstrate how to:
- Scrape economic news from a website.
- Use OpenAI’s GPT-4o API for macroeconomic analysis.
- Create an interactive web-based UI using **Streamlit**.

You can use it to experiment with financial data, AI-based analysis, or to learn how different tools like web scraping, API integrations, and data analysis come together in a web app.

### Important: 
This tool is intended **for educational purposes only** and should not be used for any financial or trading decisions.

---

## Features

- **Scraping**: Fetches macroeconomic news from TradingView’s API for Australian bonds.
- **OpenAI Integration**: Sends the news content to OpenAI’s GPT-4 API for macroeconomic analysis.
- **Streamlit Interface**: Easy-to-use, interactive UI for controlling the scraping and analysis process.
- **Customizable**: Easily modify the app to scrape data from other sources or analyze different assets.

---

## Requirements

- Python 3.x
- The following Python libraries:
  - `streamlit`
  - `requests`
  - `beautifulsoup4`
  - `openai`
  
---

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/kanalive/auto_ym.git
    cd auto_ym
    ```

## Usage

1. **Run the Streamlit app**:
    ```bash
    streamlit run streamlit_app.py
    ```

2. **Load the OpenAI API Key**:
    - When prompted, enter your OpenAI API key, please ensure it has access to the gpt-4o model.

3. **Fetch and Analyze News**:
    - Choose the time window for fetching news.
    - Click the **Fetch and Analyze** button to scrape the news and get predictions for tomorrow's trading bias based on the latest macroeconomic data.

---

## License

This project is provided under the MIT License, allowing for open sharing and modification of the code.

---

**Disclaimer**: This tool is provided as a learning resource only. It is not intended for financial trading or investment purposes. Use at your own risk.
