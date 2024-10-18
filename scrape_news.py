import requests
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

class TradingViewNewsScraper:
    def __init__(self, symbol="TVC:AU03Y", lang="en", time_window=24):
        # Initialize with default symbol, language, and time window (in hours)
        self.symbol = symbol
        self.lang = lang
        self.time_window = time_window
        self.base_url = f'https://news-headlines.tradingview.com/v2/view/headlines/symbol?client=overview&lang={self.lang}&symbol={self.symbol}'
        self.news_to_scrape = []

    def fetch_news(self):
        # Fetch the JSON data from the TradingView news API
        response = requests.get(self.base_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch news for symbol: {self.symbol}")
            return None

    def filter_recent_news(self, news_items):
        # Filter news articles based on the time window (e.g., last 24 hours)
        current_time = time.time()
        time_threshold = current_time - (self.time_window * 60 * 60)

        for item in news_items:
            published_time = item.get('published')
            if published_time and published_time >= time_threshold:
                story_path = item.get('storyPath')
                if story_path:
                    full_url = f"https://www.tradingview.com{story_path}"
                    self.news_to_scrape.append(full_url)

    def scrape_news_content(self, news_url):
        # Scrape the content of a news article
        response = requests.get(news_url)
        if response.status_code != 200:
            return f"Failed to fetch content from {news_url}"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        story_content_div = soup.find('div', {'data-name': 'news-story-content'})

        if not story_content_div:
            return "No content found."

        p_tags = story_content_div.find_all('p')
        content = " ".join(p.get_text(strip=True) for p in p_tags if p.get_text(strip=True))

        return content if content else "No content found."

    def get_news(self):
        # Main method to fetch, filter, and scrape news
        news_data = self.fetch_news()
        if not news_data:
            return []

        news_items = news_data.get('items', [])
        self.filter_recent_news(news_items)
        scraped_news = []

        for news_url in self.news_to_scrape:
            print(f"Scraping content from: {news_url}")
            news_content = self.scrape_news_content(news_url)
            scraped_news.append({
                'url': news_url,
                'content': news_content
            })

        return scraped_news
