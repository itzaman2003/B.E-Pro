# moneycontrol_scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_moneycontrol_news():
    url = "https://www.moneycontrol.com/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find news items - adjust this selector as per site structure
    articles = soup.find_all("div", class_="clearfix")
    
    data = []
    for article in articles[:10]:  # limiting to top 10 articles
        title_tag = article.find("a")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        link = title_tag.get('href')
        description = article.find("p")
        description_text = description.get_text(strip=True) if description else ""
        
        data.append({
            "title": title,
            "description": description_text,
            "url": link
        })
    return pd.DataFrame(data)
