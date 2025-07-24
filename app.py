import streamlit as st
import snscrape.modules.twitter as sntwitter
from textblob import TextBlob
import nltk

nltk.download('punkt')

st.set_page_config(page_title="Sentiment Scanner", layout="centered")

st.title("🧠 Sentiment Scanner")
st.write("Analyse des tweets crypto pour déduire une position **LONG/SHORT**")

query = st.text_input("🔍 Entre le nom ou ticker d'une crypto-monnaie :", value="$DOGE")

def get_tweets(query, limit=50):
    tweets = []
    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            tweets.append(tweet.content)
            if i >= limit:
                break
    except Exception as e:
        st.error(f"Erreur récupération tweets : {e}")
    return tweets

def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

if st.button("Analyser"):
    if query.strip() == "":
        st.warning("Veuillez entrer un nom de crypto.")
    else:
        tweets = get_tweets(query)
        if not tweets:
            st.error("Aucun tweet trouvé pour cette requête.")
        else:
            sentiments = [get_sentiment(t) for t in tweets]
            avg_sentiment = sum(sentiments) / len(sentiments)
            
            st.write(f"Nombre de tweets analysés : {len(tweets)}")
            st.write(f"Sentiment moyen : `{avg_sentiment:.3f}`")

            if avg_sentiment > 0.1:
                st.success("🟢 Position recommandée : LONG")
            elif avg_sentiment < -0.1:
                st.error("🔴 Position recommandée : SHORT")
            else:
                st.warning("🟡 Position recommandée : NEUTRE")