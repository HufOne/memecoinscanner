import streamlit as st
import tweepy
from textblob import TextBlob
import nltk
import os # Ajouté pour potentiellement lire les variables d'environnement si tu ne passes pas par st.secrets

#--- Gestion du téléchargement NLTK ---
# Répertoire où NLTK va chercher/stocker ses données
nltk_data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)) , 'nltk_data')

# Si le répertoire n'existe pas, crée-le
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)

# Pointe NLTK vers ce répertoire
nltk.data.path.append(nltk_data_dir)

# Télécharge 'punkt' si ce n'est pas déjà fait
try:
    # Vérifie si 'punkt' est déjà dans le chemin NLTK
    nltk.data.find('tokenizers/punkt')
except LookupError: # LookupError est l'exception correcte pour les données NLTK manquantes
    st.info("Téléchargement du package NLTK 'punkt' (première fois seulement)...")
    nltk.download('punkt', download_dir=nltk_data_dir)
    st.success("Package 'punkt' téléchargé.")

st.set_page_config(page_title="Sentiment Scanner", layout="centered")

st.title("🧠 Sentiment Scanner")
st.write("Analyse des tweets crypto pour déduire une position **LONG/SHORT**")

# --- Configuration de l'API Twitter ---
# Pour la sécurité, il est FORTEMENT recommandé d'utiliser st.secrets
# si tu déploies sur Streamlit Cloud, ou des variables d'environnement.
# Pour le développement local, tu peux les mettre directement ici pour tester,
# MAIS PENSE À LES RETIRER AVANT DE POUSSER SUR UN DÉPÔT PUBLIC !

# Si tu utilises st.secrets (recommandé pour Streamlit Cloud) :
try:
  import os # Assure-toi que 'os' est bien importé en haut du fichier

... (le reste de ton code)
Accède au secret via les variables d'environnement de Codespaces
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

if not BEARER_TOKEN:
    st.error("La clé Bearer Token Twitter n'est pas configurée dans les secrets de Codespaces.")
    st.stop()
except KeyError:
    st.error("Les clés API Twitter ne sont pas configurées dans `secrets.toml` ou variables d'environnement.")
    st.stop() # Arrête l'exécution si les clés ne sont pas trouvées

# Si tu n'utilises PAS st.secrets, et que tu veux lire depuis les variables d'environnement (pour un déploiement non-Streamlit Cloud par exemple)
# BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
# if not BEARER_TOKEN:
#     st.error("La variable d'environnement TWITTER_BEARER_TOKEN n'est pas définie.")
#     st.stop()


# Initialisation du client Tweepy pour l'API v2
try:
    client = tweepy.Client(BEARER_TOKEN)
    # Si tu utilises l'API v1.1 (pour certaines opérations spécifiques)
    # auth_v1 = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # api_v1 = tweepy.API(auth_v1, wait_on_rate_limit=True)
except Exception as e:
    st.error(f"Erreur d'initialisation de l'API Twitter. Vérifie tes clés. Détails : {e}")
    st.stop()

query_input = st.text_input("🔍 Entre le nom ou ticker d'une crypto-monnaie :", value="$DOGE")

def get_tweets_from_twitter_api(query, limit=50):
    tweets_content = []
    try:
        # L'API v2 de Twitter avec le compte gratuit permet 100 tweets max par requête et 7 jours d'historique.
        # Nous prenons le minimum entre la limite demandée et 100.
        response = client.search_recent_tweets(
            query + " -is:retweet",
            tweet_fields=["text"], # Demande le champ 'text' pour le contenu du tweet
            max_results=min(limit, 100)
        )

        if response.data:
            for tweet in response.data:
                tweets_content.append(tweet.text)
        else:
            st.warning(f"Aucun tweet trouvé ou problème avec la requête pour '{query}'. Vérifie l'orthographe ou essaie un autre terme.")

    except tweepy.TweepyException as e:
        st.error(f"Erreur de récupération des tweets via l'API Twitter : {e}")
        st.info("Vérifie tes quotas d'API Twitter ou le terme de recherche.")
    except Exception as e:
        st.error(f"Une erreur inattendue est survenue lors de la récupération des tweets : {e}")
    return tweets_content

def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

if st.button("Analyser"):
    if query_input.strip() == "":
        st.warning("Veuillez entrer un nom de crypto.")
    else:
        tweets = get_tweets_from_twitter_api(query_input, limit=50) # Utilise la nouvelle fonction

        if not tweets:
            st.error("Aucun tweet valide trouvé pour cette requête ou problème d'API. Assure-toi que les clés API sont correctes et que des tweets existent pour le terme de recherche.")
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

