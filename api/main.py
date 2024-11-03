import requests
from bs4 import BeautifulSoup
import json

# URL de la page cible
url = "https://www.podcastfrancaisfacile.com/texte"

# Effectuer la requête HTTP pour récupérer le contenu de la page
response = requests.get(url)
response.raise_for_status()

# Analyse de la page avec BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Liste pour stocker les informations d'articles
data = []

# Recherche de toutes les sections d'articles
articles = soup.find_all('article')  # Vérifiez et adaptez cette balise selon la structure HTML

for article in articles:
    # Récupération du texte complet de l'article
    article_text = article.get_text(separator="\n").strip()
    
    # Récupération de l'URL de la première image de l'article
    image_tag = article.find('img')
    image_url = image_tag['src'] if image_tag else None

    # Ajouter les informations dans la liste des données
    data.append({
        'image_url': image_url,
        'article_text': article_text
    })

# Conversion en JSON
output = json.dumps(data, ensure_ascii=False, indent=4)
print(output)
