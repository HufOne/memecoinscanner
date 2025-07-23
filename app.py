
import streamlit as st
import requests
import pandas as pd
from textblob import TextBlob
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# === Configuration de la page ===
st.set_page_config(page_title="MemeCoin Sentiment Scanner", layout="wide", page_icon="📈")

# === Clé API Bearer de Twitter fournie par l'utilisateur ===
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACfQ3AEAAAAAZM4T%2Bb%2FyeBb%2BiH17aQ%2FbH%2FdbrSg%3D6RFB0O1YIh0yMARKn1g1IOpcGc4otT9DoVjrUcC63g22ZtyWjI"
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

# === Requête API Twitter ===
def search_tweets(query, max_results=50):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {
        "query": query + " lang:en -is:retweet",
        "max_results": max_results,
        "tweet.fields": "created_at,text"
    }
    response = requests.get(search_url, headers=headers, params=query_params)
    if response.status_code != 200:
        st.error("Erreur API Twitter")
        return []
    return response.json().get("data", [])

# === Nettoyage des tweets ===
def clean_tweet(tweet):
    tweet = re.sub(r"http\S+", "", tweet)
    tweet = re.sub(r"@\S+", "", tweet)
    tweet = re.sub(r"#", "", tweet)
    return tweet.strip()

# === Analyse de sentiment avec TextBlob ===
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# === Interface utilisateur ===
st.markdown("<h1 style='color:white;'>📊 MemeCoin Sentiment Scanner</h1>", unsafe_allow_html=True)
st.markdown("<small style='color:gray;'>Analyse des tweets crypto pour déduire une position LONG/SHORT</small>", unsafe_allow_html=True)
st.markdown("---")

query = st.text_input("🔍 Entre le nom ou ticker d'une crypto-monnaie :", value="$DOGE")

if query:
    with st.spinner("Analyse en cours..."):
        tweets = search_tweets(query)
        if tweets:
            df = pd.DataFrame(tweets)
            df["clean_text"] = df["text"].apply(clean_tweet)
            df["polarity"] = df["clean_text"].apply(analyze_sentiment)

            avg_sentiment = df["polarity"].mean()
            sentiment_score = round((avg_sentiment + 1) / 2 * 100, 2)

            position = "LONG 📈" if avg_sentiment > 0.05 else "SHORT 📉" if avg_sentiment < -0.05 else "NEUTRE ⚖️"

            st.markdown(f"### 🧠 Position suggérée : **{position}**")
            st.markdown(f"**Score de confiance :** {sentiment_score}%")
            st.markdown("---")

            all_words = " ".join(df["clean_text"])
            wordcloud = WordCloud(width=800, height=300, background_color='black', colormap='plasma').generate(all_words)
            st.markdown("#### ☁️ Mots-clés dominants :")
            st.image(wordcloud.to_array())

            st.markdown("#### 🗨️ Tweets analysés :")
            for i, row in df.iterrows():
                st.markdown(f"- *{row['clean_text']}*")
        else:
            st.warning("Aucun tweet trouvé pour cette requête.")
else:
    st.info("Entrez un mot-clé ou un ticker pour lancer l'analyse.")
