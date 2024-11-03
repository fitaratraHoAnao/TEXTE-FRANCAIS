from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# URL de base de la page cible
BASE_URL = "https://www.podcastfrancaisfacile.com/texte"

def get_articles(page=1):
    # Construire l'URL pour la pagination
    url = f"{BASE_URL}/page/{page}" if page > 1 else BASE_URL
    print(f"Fetching URL: {url}")  # Debug : affiche l'URL

    # Effectuer la requête HTTP
    response = requests.get(url)
    response.raise_for_status()

    # Analyse de la page avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    articles_data = []

    # Rechercher les articles sur la page
    articles = soup.find_all('article')
    print(f"Found {len(articles)} articles on page {page}")  # Debug : nombre d'articles trouvés

    for index, article in enumerate(articles, start=1):
        # Récupérer le texte de l'article
        article_text = article.get_text(separator="\n").strip()

        # Récupérer l'URL de l'image
        image_tag = article.find('img')
        image_url = image_tag['src'] if image_tag else None

        # Ajouter l'article et l'URL de l'image avec numérotation
        articles_data.append({
            'numero': index,
            'article_text': article_text,
            'image_url': image_url
        })

    return articles_data

# Route pour afficher tous les articles avec pagination
@app.route('/affiche', methods=['GET'])
def affiche():
    # Récupérer le paramètre `page`
    page = request.args.get('page', 1, type=int)

    # Extraire les articles pour la page demandée
    articles = get_articles(page=page)

    # Retourner les résultats en format JSON avec la pagination
    return jsonify({
        'page': page,
        'articles': articles
    })

# Lancer l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
