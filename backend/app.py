from flask import Flask, request, jsonify
import requests
import os
from fetch_location import get_nearby_wikipedia_articles, format_fun_fact

app = Flask(__name__)

@app.route('/get_fun_fact', methods=['GET'])
def get_fun_fact():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({'error': 'Missing latitude or longitude'}), 400
    
    articles = get_nearby_wikipedia_articles(lat, lon)
    
    if not articles:
        return jsonify({'error': 'No articles found nearby'}), 404

    # Generate a fun fact based on the first article found
    article = articles[0]
    article_title = article['title']
    article_distance = article['dist']
    fun_fact = format_fun_fact(article_title)
    article_url = f"https://en.wikipedia.org/wiki/{article_title.replace(' ', '_')}"
    
    response_text = f"Fun Fact at {article_distance} meters from you: {fun_fact}. Read more about this fact at: {article_url}"
    
    return jsonify({'fun_fact': response_text})

if __name__ == '__main__':
    app.run(debug=True)
