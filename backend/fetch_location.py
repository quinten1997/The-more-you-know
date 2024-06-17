import requests
import os
from transformers import pipeline, set_seed

# Initialize the GPT-2 model
generator = pipeline('text-generation', model='gpt2')
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

def format_fun_fact(fact_text):
    generated_texts = generator(fact_text, max_length=50, num_return_sequences=1)
    formatted_text = generated_texts[0]['generated_text']
    return formatted_text
