# Sentiment Scanner

Application Streamlit d'analyse de sentiment pour les crypto-monnaies à partir de tweets Twitter/X via `snscrape`.

## Utilisation

1. Entrez un nom ou ticker de crypto-monnaie (ex: `$DOGE`, `$PEPE`).
2. Cliquez sur "Analyser".
3. Obtenez une position recommandée : LONG, SHORT ou NEUTRE.

## Déploiement

### Local
```bash
pip install -r requirements.txt
streamlit run app.py
```

### GitHub + Streamlit Cloud
1. Poussez ce dossier sur GitHub.
2. Allez sur [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Connectez votre repo GitHub et sélectionnez `app.py` comme script principal.
