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

    for article in articles:
        # Récupérer le texte de l'article
        article_text = article.get_text(separator="\n").strip()
        
        # Récupérer l'URL de l'image
        image_tag = article.find('img')
        image_url = image_tag['src'] if image_tag else None

        # Ajouter l'article et l'URL de l'image
        articles_data.append({
            'image_url': image_url,
            'article_text': article_text
        })
    
    return articles_data

# Route pour effectuer la recherche avec pagination et texte fixe
@app.route('/recherche', methods=['GET'])
def recherche():
    # Récupérer les paramètres `titre` et `page`
    titre = request.args.get('titre', '')
    page = request.args.get('page', 1, type=int)
    
    # Extraire les articles pour la page demandée
    articles = get_articles(page=page)

    # Filtrer les articles par le texte recherché s'il est spécifié
    if titre:
        articles = [a for a in articles if titre.lower() in a['article_text'].lower()]

    # Retourner les résultats en format JSON avec la pagination
    return jsonify({
        'page': page,
        'search_text': titre,
        'articles': articles
    })

# Lancer l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
