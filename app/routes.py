from flask import Blueprint, render_template, request, jsonify
from app.pico_pubmed import (parse_pico_with_cohere, summarize_paper_with_cohere, classify_question)
from .data import articles_case_1, articles_case_2  # Import the articles data structure
import cohere
import os

main = Blueprint('main', __name__)

# Initialize Cohere client for routes
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Debug print to confirm deployed version
print("===== ROUTES.PY: Updated for Cohere Chat API =====")

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
        print(f"Question type: {question_type}")
        
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

    prompt = (
        "Rewrite the following question as a clear, well-structured PICO question:\n\n"
        f"{original_question}"
    )

    # CHANGED: co.generate() -> co.chat()
    response = co.chat(
        model='command-a-03-2025',
        message=prompt,  # CHANGED: prompt -> message
        temperature=0.7
    )

    return jsonify({
        "suggested_question": response.text.strip()
    })


# Add a debug route to verify the API is working
@main.route('/test-cohere')
def test_cohere():
    """Test route to verify Cohere Chat API is working"""
    try:
        # Simple test with chat API
        response = co.chat(
            model='command-a-03-2025',
            message='Hello, are you working?',
            temperature=0
        )
        return jsonify({
            'status': 'success',
            'cohere_response': response.text,
            'api_used': 'chat'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'cohere_version': cohere.__version__ if hasattr(cohere, '__version__') else 'unknown'
        })