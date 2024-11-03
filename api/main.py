from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# URL de base de la page cible
BASE_URL = "https://www.podcastfrancaisfacile.com/texte"

# Route pour rechercher un texte spécifique
@app.route('/recherche', methods=['GET'])
def recherche():
    # Récupération du titre depuis le paramètre de requête
    titre = request.args.get('titre')
    if not titre:
        return jsonify({'error': 'Veuillez fournir un titre.'}), 400

    # Construction de l'URL de la page à scraper
    url = f'{BASE_URL}/{titre}.html'

    try:
        # Requête pour obtenir le contenu HTML de la page
        response = requests.get(url)
        response.encoding = 'utf-8'  # Assurez-vous que l'encodage est correct
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraction du texte principal
        main_content = soup.find('div', class_='post-content')
        if not main_content:
            return jsonify({'error': "Le contenu principal n'a pas été trouvé."}), 404

        # Extraction du texte
        paragraphs = main_content.find_all('p')
        texte = [para.get_text() for para in paragraphs]

        # Extraction du vocabulaire si présent
        vocab_section = main_content.find_all('strong')
        vocabulaire = [vocab.get_text() for vocab in vocab_section]

        return jsonify({
            'titre': titre,
            'texte': texte,
            'vocabulaire': vocabulaire
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erreur de requête: {str(e)}'}), 500

# Fonction pour récupérer les articles d'une page donnée avec numérotation
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

# Route pour afficher tous les articles avec pagination et numérotation
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
