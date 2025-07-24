# 🧠 MemeCoin Sentiment Scanner

Analyse automatique de sentiment autour des cryptos (notamment **meme coins**) à partir de **tweets Twitter/X**.

> Basé sur `snscrape` et `TextBlob` pour contourner les limitations de l'API Twitter.

---

## 🚀 Fonctionnalités

- 🔍 Recherche de tweets récents contenant un symbole crypto (ex: `$PEPE`, `$DOGE`, `$PENGU`)
- 💬 Analyse de **sentiment** : positif, neutre ou négatif
- 📊 Recommandation de **position trading** : LONG, SHORT ou NEUTRE
- 100% open-source et hébergeable gratuitement

---

## 📦 Technologies

- `Streamlit` – Interface web ultra légère
- `snscrape` – Récupération de tweets sans clé API
- `TextBlob` – Analyse de sentiment
- `nltk` – Tokenisation linguistique

---

## 🛠️ Installation locale

```bash
git clone https://github.com/<ton-user>/memecoinscanner.git
cd memecoinscanner
pip install -r requirements.txt
streamlit run app.py
