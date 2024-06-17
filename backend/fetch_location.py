import requests
import os
from transformers import pipeline, set_seed

# Initialize the GPT-2 model for text generation and summarization
generator = pipeline('text-generation', model='gpt2')
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
set_seed(42)

def get_nearby_wikipedia_articles(lat, lon, radius=500):
    url = os.getenv('WIKIPEDIA_API_URL', 'https://en.wikipedia.org/w/api.php')
    params = {
        'action': 'query',
        'list': 'geosearch',
        'gscoord': f'{lat}|{lon}',
        'gsradius': radius,
        'gslimit': 10,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('query', {}).get('geosearch', [])
    else:
        return []

def format_fun_fact(article_title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{article_title}"
    response = requests.get(url)
    if response.status_code == 200:
        summary = response.json().get('extract', '')
    else:
        summary = f"Details about {article_title}."

    # Summarize the fact to ensure it is no longer than 200 words
    summarized_texts = summarizer(summary, max_length=200, min_length=30, do_sample=False)
    formatted_text = summarized_texts[0]['summary_text']
    return formatted_text
