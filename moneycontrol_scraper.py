from newspaper import Article
import pandas as pd

# Top Moneycontrol news URLs (can be extended)
moneycontrol_urls = [
    # Corporate News
    "https://www.moneycontrol.com/news/business/",
    "https://www.moneycontrol.com/news/companies/",
    "https://www.moneycontrol.com/news/business/ceo-talk/",

    # Market Updates
    "https://www.moneycontrol.com/news/markets/",
    "https://www.moneycontrol.com/news/market-edge/",
    "https://www.moneycontrol.com/news/stocks/",
    "https://www.moneycontrol.com/news/fii-dii-data/",

    # Economic News
    "https://www.moneycontrol.com/news/economy/",
    "https://www.moneycontrol.com/news/economy/indian-economy/",

    # Government Policies
    "https://www.moneycontrol.com/news/budget/",
    "https://www.moneycontrol.com/news/policy/",

    # New IPOs
    "https://www.moneycontrol.com/news/ipo/",

    # Debt Issues
    "https://www.moneycontrol.com/news/bonds/",
    "https://www.moneycontrol.com/news/finance/",

    # Industry News
    "https://www.moneycontrol.com/news/automobile/",
    "https://www.moneycontrol.com/news/pharma/",
    "https://www.moneycontrol.com/news/telecom/",
    "https://www.moneycontrol.com/news/banks/",
    "https://www.moneycontrol.com/news/real-estate/",
    "https://www.moneycontrol.com/news/fmcg/",

    # Currency/Forex
    "https://www.moneycontrol.com/news/forex/",

    # Commodities
    "https://www.moneycontrol.com/news/commodities/",

    # Mergers & Acquisitions
    "https://www.moneycontrol.com/news/business/mergers-acquisitions/",

    # Startups & Venture Capital
    "https://www.moneycontrol.com/news/business/startup/",
    "https://www.moneycontrol.com/news/trends/startup/",

    # Banking & Finance
    "https://www.moneycontrol.com/news/banks/",
    "https://www.moneycontrol.com/news/finance/",
    "https://www.moneycontrol.com/news/insurance/",
    "https://www.moneycontrol.com/news/mutual-funds/",
    "https://www.moneycontrol.com/news/personal-finance/",
    "https://www.moneycontrol.com/news/tax/",

    # Technology & Innovation
    "https://www.moneycontrol.com/news/technology/",
    "https://www.moneycontrol.com/news/business/tech-bytes/",

    # ESG & Sustainability
    "https://www.moneycontrol.com/news/environment/",
    "https://www.moneycontrol.com/news/world/environmental-social-governance-esg/",

    # Global Markets
    "https://www.moneycontrol.com/news/world/",
    "https://www.moneycontrol.com/news/us-markets/",
    "https://www.moneycontrol.com/news/international-markets/",

    # General / Other News
    "https://www.moneycontrol.com/news/trends/current-affairs/",
    "https://www.moneycontrol.com/news/health-and-fitness/",
    "https://www.moneycontrol.com/news/lifestyle/",
    "https://www.moneycontrol.com/news/politics/",
    "https://www.moneycontrol.com/news/sports/",
    "https://www.moneycontrol.com/news/technology/science/"
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

