from flask import Blueprint, render_template, request, jsonify
from app.pico_pubmed import (parse_pico_with_cohere, summarize_paper_with_cohere, classify_question)
from .data import articles_case_1, articles_case_2  # Import the articles data structure
import cohere
import os

main = Blueprint('main', __name__)

# Define the path to the PDF folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "pdf_dataset")

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/pico-question', methods=['GET', 'POST'])
def pico_question():
    if request.method == 'POST':
        pico_question = request.form['pico_question']

         # Parse the PICO components
        parsed_pico = parse_pico_with_cohere(pico_question)
        
        # Classify the question using the cohere function
        question_type = classify_question(pico_question)
        print(classify_question(pico_question))
        
        if question_type == 'case1':
            articles = articles_case_1
        elif question_type == 'case2':
            articles = articles_case_2
        else:
            articles = []
        
        results = []
        
        # Process all articles in the data structure
        for article in articles:
            # Summarize each article's abstract
            summary = summarize_paper_with_cohere(article['abstract'])
            
            # Append details including score
            results.append({
                'title': article['title'],
                'url': article['url'],
                'abstract': article['abstract'],
                'summary': summary,
                'score': article['score']
            })
        
        # Sort results by score in descending order
        # Sort results by score in descending order, then reverse alphabetically by title
        results = sorted(results, key=lambda x: (-x['score'], -ord(x['title'][0].lower())))
        
        return jsonify({
            'pico': parsed_pico,
            'results': results,
            'pico_question': pico_question
        })
    
    return render_template('pico_question.html')

@main.route('/help-pico', methods=['POST'])
def help_pico():
    data = request.json
    original_question = data['original_question']
    
    prompt = f"Rewrite the following question as a well-structured PICO question: '{original_question}'"
    response = co.generate(
        model='command',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        k=0,
        stop_sequences=[],
        return_likelihoods='NONE'
    )
    suggested_question = response.generations[0].text.strip()
    
    return jsonify({'suggested_question': suggested_question})