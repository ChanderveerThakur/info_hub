import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

API_KEY = os.getenv('NEWS_API_KEY')
PROVIDER = os.getenv('NEWS_PROVIDER', 'newsapi')


def fetch_news(query, language='en'):
    """
    Fetches news articles with title, description, url, source, publishedAt, and image.
    Supports both NewsAPI.org and NewsData.io.
    """
    query = query or 'latest'
    try:
        if PROVIDER == 'newsapi':
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': query,
                'language': language,
                'sortBy': 'publishedAt',
                'apiKey': API_KEY,
                'pageSize': 20
            }
        else:
            url = 'https://newsdata.io/api/1/news'
            params = {
                'q': query,
                'language': language,
                'apikey': API_KEY,
                'page': 1
            }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        # Different key names for different APIs
        articles = data.get('articles') or data.get('results', [])
        result = []
        for a in articles:
            result.append({
                'title': a.get('title'),
                'description': a.get('description'),
                'url': a.get('url') or a.get('link'),
                'source': (a.get('source') or {}).get('name') or a.get('source_id'),
                'publishedAt': a.get('publishedAt') or a.get('pubDate'),
                # ✅ poster image for each news
                'image': a.get('urlToImage') or a.get('image_url')
            })
        return result

    except Exception as e:
        print("⚠️ Error fetching news:", e)
        return []
