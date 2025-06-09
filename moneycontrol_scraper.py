from newspaper import Article
import pandas as pd

moneycontrol_urls = [
    "https://www.moneycontrol.com/news/business/",
    "https://www.moneycontrol.com/news/economy/",
    "https://www.moneycontrol.com/news/markets/",
    "https://www.moneycontrol.com/news/finance/"
]

def fetch_moneycontrol_news():
    articles_data = []
    for url in moneycontrol_urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            articles_data.append({
                "title": article.title,
                "description": article.text[:300],
                "url": url
            })
        except Exception as e:
            print("❌ Error:", e)
            continue
    return pd.DataFrame(articles_data)
