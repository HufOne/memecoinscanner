import streamlit as st # S'assurer que streamlit est bien importé au début
import tweepy
from textblob import TextBlob
import nltk
import os # S'assurer que os est bien importé au début

# --- Gestion du téléchargement NLTK ---
# Définit le répertoire où NLTK stockera les données
nltk_data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'nltk_data')

# Si le répertoire n'existe pas, crée-le
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)

# Ajoute ce répertoire au chemin de recherche de NLTK
nltk.data.path.append(nltk_data_dir)

# Tente de trouver 'punkt'. S'il n'est pas trouvé, le télécharge.
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    st.info("Téléchargement du package NLTK 'punkt' (première fois seulement)...")
    nltk.download('punkt', download_dir=nltk_data_dir)
    st.success("Package 'punkt' téléchargé.")

st.set_page_config(page_title="Sentiment Scanner", layout="centered")

# ... (le reste de ton code, y compris la configuration de l'API Twitter) ...

st.title("🧠 Sentiment Scanner")
st.write("Analyse des tweets crypto pour déduire une position **LONG/SHORT**")

# ... (ton code NLTK et Streamlit set_page_config, titre, etc. ici, inchangé)

st.set_page_config(page_title="Sentiment Scanner", layout="centered")

st.title("🧠 Sentiment Scanner")
st.write("Analyse des tweets crypto pour déduire une position **LONG/SHORT**")

# ... (le code précédent de NLTK, st.set_page_config, titres, etc.)

st.set_page_config(page_title="Sentiment Scanner", layout="centered")

st.title("🧠 Sentiment Scanner")
st.write("Analyse des tweets crypto pour déduire une position **LONG/SHORT**")

# --- Configuration de l'API Twitter ---
# Récupère le Bearer Token depuis les variables d'environnement du Codespace (ou de Streamlit Cloud si déployé là)
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Vérifie si la clé est présente. Si elle ne l'est pas, arrête l'application avec un message d'erreur.
if BEARER_TOKEN is None:
    st.error("ERREUR : La clé Bearer Token Twitter (TWITTER_BEARER_TOKEN) n'est pas configurée.")
    st.info("Veuillez la définir comme un secret dans les paramètres de votre Codespace GitHub.")
    st.stop() # Arrête l'exécution de l'application Streamlit

# Initialise le client Tweepy avec le Bearer Token
# Utilisez un bloc try-except ici pour capturer les erreurs d'initialisation de l'API.
try:
    client = tweepy.Client(BEARER_TOKEN)
    # Optionnel : Faire une petite requête de test pour s'assurer que le client fonctionne
    # try:
    #     client.get_me() # Tente de récupérer les informations de l'utilisateur authentifié
    # except Exception as e:
    #     st.error(f"ERREUR : Le Bearer Token est configuré mais invalide. Détails : {e}")
    #     st.stop()
except Exception as e:
    st.error(f"ERREUR : Impossible d'initialiser l'API Twitter (Tweepy Client).")
    st.error(f"Détails de l'erreur : {e}")
    st.stop() # Arrête l'application si le client ne peut pas être créé

# ... (le reste de ton code d'application : query_input, fonctions, bouton Analyser, etc.)
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

