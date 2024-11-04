from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# URL de base de la page cible
BASE_URL = "https://www.podcastfrancaisfacile.com/texte"

# Fonction pour récupérer les articles d'une page donnée avec nettoyage du texte
def get_articles(page=1):
    # Construire l'URL pour la pagination
    url = f"{BASE_URL}/page/{page}" if page > 1 else BASE_URL
    response = requests.get(url)
    response.raise_for_status()

    # Analyse de la page avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    articles_data = []

    # Rechercher les articles sur la page
    articles = soup.find_all('article')

    for index, article in enumerate(articles, start=1):
        # Récupérer et nettoyer le texte de l'article
        article_text = article.get_text(separator=" ").strip()
        article_text = ' '.join(article_text.split())  # Supprime les espaces/sauts de ligne en excès

        # Supprimer les informations inutiles (nom de l'auteur, date, catégories, etc.)
        unwanted_parts = ["Vincent Durrenberger", "Catégories :", "Mots-clés :"]
        for part in unwanted_parts:
            article_text = article_text.replace(part, "")

        # Récupérer l'URL de l'image si elle existe
        image_tag = article.find('img')
        image_url = image_tag['src'] if image_tag else None

        # Ajouter l'article et l'URL de l'image avec numérotation
        articles_data.append({
            'numero': index,
            'article_text': article_text,
            'image_url': image_url
        })

    return articles_data

# Route pour afficher tous les articles avec pagination et nettoyage
@app.route('/affiche', methods=['GET'])
def affiche():
    # Récupérer le paramètre `page`
    page = request.args.get('page', 1, type=int)

    # Extraire les articles pour la page demandée
    articles = get_articles(page=page)

    # Retourner les résultats en format JSON
    return jsonify({
        'page': page,
        'articles': articles
    })

# Lancer l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
