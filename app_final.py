import pandas as pd
import streamlit as st
from textblob import TextBlob
import nltk
import spacy
import plotly.express as px
from moneycontrol_scraper import fetch_moneycontrol_news
from pymongo import MongoClient
import subprocess
import sys



# Download required NLP resources
nltk.download('punkt')
nltk.download('stopwords')
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["finance_news_db"]
collection = db["articles"]

# Streamlit app config
st.set_page_config(page_title="Financial News Analyzer", layout="wide")
st.title("📈 Financial News Analyzer")
st.caption("Real-time news aggregation, sentiment analysis & topic classification from Moneycontrol.")

# Fetch news
@st.cache_data(ttl=600)
def fetch_news():
    return fetch_moneycontrol_news()

# Sentiment analysis
def get_sentiment(text):
    if pd.isna(text): return "Neutral"
    polarity = TextBlob(text).sentiment.polarity
    return "Positive" if polarity > 0.1 else "Negative" if polarity < -0.1 else "Neutral"

# Entity extraction
def extract_entities(text):
    if pd.isna(text): return ""
    doc = nlp(text)
    return ", ".join([ent.text for ent in doc.ents if ent.label_ in ["ORG", "MONEY", "GPE", "PRODUCT"]])

# Topic classification
topic_keywords = {
    "Corporate News": [
        "corporate", "merger", "acquisition", "business", "ceo", "executive", "board of directors",
        "leadership change", "quarterly results", "earnings report", "subsidiary", "strategic partnership"
    ],
    "Market Updates": [
        "sensex", "nifty", "market", "stocks", "shares", "trading", "bse", "nse", "indices", "benchmark", 
        "closing bell", "market rally", "bullish", "bearish", "volatility"
    ],
    "Economic News": [
        "economy", "gdp", "inflation", "recession", "macroeconomic", "economic slowdown", "economic growth",
        "unemployment", "fiscal deficit", "economic indicators", "current account", "balance of payments"
    ],
    "Government Policies": [
        "rbi", "budget", "policy", "regulation", "ministry", "government", "tax reform", "monetary policy",
        "fiscal policy", "parliament", "cabinet", "incentives", "subsidies", "infrastructure policy"
    ],
    "New IPOs": [
        "ipo", "initial public offering", "listing", "draft red herring prospectus", "SEBI approval",
        "pre-ipo", "grey market premium", "public issue", "subscription", "book building"
    ],
    "Debt Issues": [
        "debt", "bond", "default", "interest payment", "borrowing", "repayment", "credit rating",
        "debenture", "loan", "sovereign debt", "yields", "bond auction", "refinancing"
    ],
    "Industry News": [
        "sector", "industry", "automobile", "pharma", "telecom", "banking", "real estate", "it sector",
        "manufacturing", "fmcg", "hospitality", "aviation", "retail", "energy sector"
    ],
    "Currency/Forex": [
        "rupee", "dollar", "currency", "forex", "exchange rate", "usd/inr", "currency reserves",
        "currency depreciation", "devaluation", "forex reserves", "currency trading"
    ],
    "Commodities": [
        "oil", "gold", "silver", "commodity", "crude", "metal", "natural gas", "copper", "commodity trading",
        "precious metals", "futures", "commodity prices", "agriculture commodities"
    ],
    "Mergers & Acquisitions": [
        "merger", "acquisition", "takeover", "buyout", "deal", "strategic acquisition", 
        "merger deal", "hostile takeover", "reverse merger"
    ],
    "Startups & Venture Capital": [
        "startup", "venture capital", "funding", "seed round", "series a", "series b", "valuation",
        "angel investor", "pitch", "incubator", "accelerator", "exit strategy"
    ],
    "Banking & Finance": [
        "banking", "nbfc", "interest rates", "loans", "credit", "mortgage", "bank", 
        "monetary tightening", "repo rate", "financial services", "asset management", "npas"
    ],
    "Technology & Innovation": [
        "technology", "ai", "machine learning", "blockchain", "fintech", "cybersecurity", "tech startup",
        "digital transformation", "software", "cloud computing", "5g"
    ],
    "ESG & Sustainability": [
        "esg", "sustainability", "green bonds", "carbon footprint", "climate change", "renewable energy",
        "csr", "net zero", "environmental", "governance", "social impact"
    ],
    "Global Markets": [
        "us market", "nasdaq", "dow jones", "s&p 500", "european market", "asian markets", 
        "global economy", "china economy", "fed", "ecb", "global inflation", "international markets"
    ],
    "General": [
            "politics", "elections", "international relations", "diplomacy", "conflict", 
             "war", "natural disaster", "earthquake", "flood", "cyclone", "pandemic", 
             "healthcare", "covid", "environment", "climate", "education", "crime", 
              "law", "legal", "judiciary", "court ruling", "sports", "tournament", 
              "entertainment", "celebrity", "film", "movie", "award", "culture", 
             "travel", "tourism", "weather", "technology", "innovation", "science"

]
}


def classify_topic(text):
    if pd.isna(text): return "General"
    text = text.lower()
    for topic, keywords in topic_keywords.items():
        if any(word in text for word in keywords):
            return topic
    return "General"

# Load and process news
with st.spinner("🔄 Fetching news articles and performing analysis..."):
    df = fetch_news()
    if not df.empty:
        df["Sentiment"] = df["description"].apply(get_sentiment)
        df["Entities"] = df["description"].apply(extract_entities)
        df["Topic"] = df["description"].apply(classify_topic)
        st.success(f"✅ {len(df)} articles processed!")
    else:
        st.error("❌ No news articles found.")
        st.stop()

# Sidebar for Topic Selection
with st.sidebar:
    st.subheader("🗂 Filter by Topic")
    all_topics = ["All"] + sorted(df["Topic"].unique())
    selected_topic = st.selectbox("Choose Topic", all_topics)
    filtered_df = df if selected_topic == "All" else df[df["Topic"] == selected_topic]

    st.download_button(
        "📥 Download CSV",
        filtered_df.to_csv(index=False).encode('utf-8'),
        file_name="filtered_financial_news.csv",
        mime="text/csv"
    )

    if st.button("🔄 Refresh News Now"):
        st.cache_data.clear()
        st.experimental_rerun()

# UI with Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📰 Articles", "🔗 Links"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sentiment Distribution")
        sentiment_counts = filtered_df['Sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        fig1 = px.pie(sentiment_counts, names="Sentiment", values="Count", hole=0.4)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Topic Distribution")
        topic_counts = filtered_df["Topic"].value_counts().reset_index()
        topic_counts.columns = ["Topic", "Count"]
        fig2 = px.bar(topic_counts, x="Topic", y="Count", color="Topic")
        st.plotly_chart(fig2, use_container_width=True)

    from collections import Counter

    st.subheader("🏢 Top Entities (ORG/GPE/MONEY/PRODUCT)")
    all_entities = ", ".join(filtered_df["Entities"].dropna()).split(", ")
    top_entities = Counter(all_entities).most_common(10)
    entity_df = pd.DataFrame(top_entities, columns=["Entity", "Count"])
    fig_entities = px.bar(entity_df, x="Entity", y="Count", color="Entity", title="Top Named Entities")
    st.plotly_chart(fig_entities, use_container_width=True)

    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    st.subheader("🧠 Common Words (Word Cloud)")
    all_text = " ".join(filtered_df["description"].dropna().tolist())
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        stopwords=nltk.corpus.stopwords.words('english')
    ).generate(all_text)
    fig_wc, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig_wc)

with tab2:
    st.subheader("📰 Filtered News Table with Pagination")

    articles_per_page = st.selectbox("Articles per page", [5, 10, 20, 50], index=1)
    total_articles = len(filtered_df)
    total_pages = (total_articles - 1) // articles_per_page + 1

    page_number = st.number_input("Page number", min_value=1, max_value=total_pages, step=1)

    start_idx = (page_number - 1) * articles_per_page
    end_idx = start_idx + articles_per_page
    page_df = filtered_df.iloc[start_idx:end_idx]

    with st.expander(f"🔬 Showing {start_idx + 1} to {min(end_idx, total_articles)} of {total_articles} articles", expanded=True):
        st.dataframe(page_df[["title", "description", "Sentiment", "Entities", "Topic"]], use_container_width=True)


with tab3:
    st.subheader("🔗 News Article Links")
    for _, row in filtered_df.iterrows():
        st.markdown(f"- **[{row['title']}]({row['url']})** &nbsp;&nbsp; _({row['Topic']}, {row['Sentiment']})_")
