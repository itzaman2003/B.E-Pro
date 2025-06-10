# # moneycontrol_scraper.py
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# def fetch_moneycontrol_news():
#     url = "https://www.moneycontrol.com/news/"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Find news items - adjust this selector as per site structure
#     articles = soup.find_all("div", class_="clearfix")
    
#     data = []
#     for article in articles[:10]:  # limiting to top 10 articles
#         title_tag = article.find("a")
#         if not title_tag:
#             continue
#         title = title_tag.get_text(strip=True)
#         link = title_tag.get('href')
#         description = article.find("p")
#         description_text = description.get_text(strip=True) if description else ""
        
#         data.append({
#             "title": title,
#             "description": description_text,
#             "url": link
#         })
#     return pd.DataFrame(data)

from newspaper import Article
import pandas as pd

# Top Moneycontrol news URLs (can be extended)
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
                "description": article.text[:300],  # limit for analysis
                "url": url
            })
        except Exception as e:
            print("❌ Error:", e)
            continue

    df = pd.DataFrame(articles_data)
    return df
