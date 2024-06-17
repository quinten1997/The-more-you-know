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
    fact_text = f"'{article['title']}' is located nearby at a distance of {article['dist']} meters."
    fun_fact = format_fun_fact(fact_text)
    
    return jsonify({'fun_fact': fun_fact})

if __name__ == '__main__':
    app.run(debug=True)
