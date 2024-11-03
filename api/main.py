from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# URL de base de la page cible
BASE_URL = "https://www.podcastfrancaisfacile.com/texte"

# Fonction pour extraire les articles d'une page spécifique
def get_articles(page=1, search_text=None):
    # Construire l'URL de la page avec pagination
    url = f"{BASE_URL}/page/{page}" if page > 1 else BASE_URL
    print(f"Fetching URL: {url}")  # Debug: afficher l'URL utilisée

    response = requests.get(url)
    response.raise_for_status()

    # Analyse de la page avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles_data = []

    # Recherche de toutes les sections d'articles
    articles = soup.find_all('article')
    print(f"Found {len(articles)} articles on page {page}")  # Debug: afficher le nombre d'articles trouvés

    for article in articles:
        # Récupération du texte complet de l'article
        article_text = article.get_text(separator="\n").strip()
        
        # Filtrer par texte de recherche, si spécifié
        if search_text and search_text.lower() not in article_text.lower():
            continue
        
        # Récupération de l'URL de la première image de l'article
        image_tag = article.find('img')
        image_url = image_tag['src'] if image_tag else None

        # Ajouter les informations dans la liste des données
        articles_data.append({
            'image_url': image_url,
            'article_text': article_text
        })

    return articles_data

# Route pour effectuer la recherche
@app.route('/recherche', methods=['GET'])
def recherche():
    # Récupérer les paramètres `texte` et `page`
    search_text = request.args.get('texte')
    page = request.args.get('page', 1, type=int)
    
    # Obtenir les articles pour la page et le texte de recherche spécifiés
    articles = get_articles(page=page, search_text=search_text)
    
    # Retourner les résultats en format JSON
    return jsonify({
        'page': page,
        'search_text': search_text,
        'articles': articles
    })

# Démarrer l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
