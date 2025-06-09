import pandas as pd
import streamlit as st
from textblob import TextBlob
import nltk
import spacy
import plotly.express as px
from moneycontrol_scraper import fetch_moneycontrol_news
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


# Download necessary NLP resources
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

# Fetch news data (scraped from Moneycontrol)
@st.cache_data(ttl=600)
def fetch_news():
    return fetch_moneycontrol_news()

# Sentiment Analysis Function
def get_sentiment(text):
    if pd.isna(text): return "Neutral"
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# Named Entity Recognition Function
def extract_entities(text):
    if pd.isna(text): return ""
    doc = nlp(text)
    return ", ".join([ent.text for ent in doc.ents if ent.label_ in ["ORG", "MONEY", "GPE", "PRODUCT"]])

# Topic Classification using keyword mapping
topic_keywords = {
    "Corporate News": ["corporate", "merger", "acquisition", "business", "ceo", "executive"],
    "Market Updates": ["sensex", "nifty", "market", "stocks", "shares", "trading", "bse", "nse"],
    "Economic News": ["economy", "gdp", "inflation", "recession", "macroeconomic"],
    "Government Policies": ["rbi", "budget", "policy", "regulation", "ministry", "government"],
    "New IPOs": ["ipo", "initial public offering", "listing"],
    "Debt Issues": ["debt", "bond", "default", "interest payment", "borrowing"],
    "Industry News": ["sector", "industry", "automobile", "pharma", "telecom", "banking"],
    "Currency/Forex": ["rupee", "dollar", "currency", "forex", "exchange rate"],
    "Commodities": ["oil", "gold", "silver", "commodity", "crude", "metal"],
    "General": []
}

def classify_topic(text):
    if pd.isna(text): return "General"
    text = text.lower()
    for topic, keywords in topic_keywords.items():
        if any(word in text for word in keywords):
            return topic
    return "General"

# Streamlit App Configuration
st.set_page_config(page_title="Financial News Analyzer", layout="wide")
st.title("💹 Automated Financial News Aggregation, Sentiment & Topic Analysis")
st.info("Fetching and analyzing news from Moneycontrol... please wait ⏳")

# Fetch and process news
df = fetch_news()
if df.empty:
    st.error("No news articles found. Check internet or source structure.")
else:
    df["Sentiment"] = df["description"].apply(get_sentiment)
    df["Entities"] = df["description"].apply(extract_entities)
    df["Topic"] = df["description"].apply(classify_topic)
    st.success(f"✅ Fetched and analyzed {len(df)} articles!")

    # Charts Section
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Sentiment Pie Chart")
        sentiment_counts = df['Sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        fig1 = px.pie(sentiment_counts, names="Sentiment", values="Count", title="Sentiment Distribution")
        st.plotly_chart(fig1, use_container_width=True)
            
        
    with col2:
        st.subheader("📚 Topic Bar Chart")
        topic_counts = df["Topic"].value_counts().reset_index()
        fig2 = px.bar(topic_counts, x="Topic", y="count", title="Topic Distribution")
        
        # fig2 = px.bar(topic_counts, x="index", y="Topic", title="Topic Distribution", color="index")
        st.plotly_chart(fig2, use_container_width=True)

    # Topic Filter Dropdown (always show all topics)
    all_topics = [
        "All",
        "Economic News",
        "General",
        "Market Updates",
        "Corporate News",
        "Government Policies",
        "New IPOs",
        "Debt Issues",
        "Industry News",
        "Currency/Forex",
        "Commodities"
    ]
    st.subheader("🔍 Filter News by Topic")
    selected_topic = st.selectbox("Choose Topic", all_topics)
    if selected_topic != "All":
        filtered_df = df[df["Topic"] == selected_topic]
    else:
        filtered_df = df

    # Display News Details
    st.subheader("📰 News Details")
    st.dataframe(filtered_df[["title", "description", "Sentiment", "Entities", "Topic"]])

    # Display Article Links
    st.subheader("🔗 Article Links")
    for _, row in filtered_df.iterrows():
        st.markdown(f"**[{row['title']}]({row['url']})** — *{row['Topic']} | {row['Sentiment']}*")
