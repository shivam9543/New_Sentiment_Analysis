import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from deep_translator import GoogleTranslator  # ✅ googletrans ka alternative
from gtts import gTTS
from collections import Counter
import streamlit as st
import os

# Step 1: Fetch News from Yahoo
def get_yahoo_news(company, max_articles=10):
    search_url = f'https://news.search.yahoo.com/search?p={company}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    for item in soup.find_all('div', class_='NewsArticle', limit=max_articles):
        title_tag = item.find('h4')
        summary_tag = item.find('p')

        if title_tag and summary_tag:
            articles.append(summary_tag.text.strip())

    return articles

# Step 2: Perform Sentiment Analysis
def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    return "Positive" if polarity > 0.05 else "Negative" if polarity < -0.05 else "Neutral"

# Step 3: Translate Text to Hindi (Using Deep Translator)
def translate_to_hindi(text):
    return GoogleTranslator(source="auto", target="hi").translate(text)

# Step 4: Convert Hindi Text to Speech
def text_to_speech_hindi(text, filename="news_audio.mp3"):
    tts = gTTS(text=text, lang="hi")
    tts.save(filename)
    return filename

# 🚀 Streamlit App
st.title("📢 News Sentiment & Hindi Speech Generator")
company_name = st.text_input("Enter the Company Name:")

if st.button("Analyze"):
    st.write("Fetching News, Performing Sentiment Analysis, Translating to Hindi, and Generating Speech...")

    news_summaries = get_yahoo_news(company_name)
    if not news_summaries:
        st.warning("No news articles found.")
    else:
        sentiments = [analyze_sentiment(summary) for summary in news_summaries]
        sentiment_counts = dict(Counter(sentiments))
        hindi_summaries = [translate_to_hindi(summary) for summary in news_summaries]

        # Convert all summaries into Hindi speech
        combined_hindi_text = " ".join(hindi_summaries)
        speech_file = text_to_speech_hindi(combined_hindi_text)

        # Display Summaries
        st.subheader("✅ News Summaries:")
        for summary in news_summaries:
            st.write(f"- {summary}")

        # Display Sentiment Distribution
        st.subheader("✅ Sentiment Distribution:")
        for sentiment, count in sentiment_counts.items():
            st.write(f"{sentiment}: {count}")

        # Play and Download Hindi Speech
        st.subheader("🎙 Hindi Speech Output:")
        st.audio(speech_file, format="audio/mp3")
        with open(speech_file, "rb") as file:
            st.download_button("Download Audio", file, file_name="news_audio.mp3")
