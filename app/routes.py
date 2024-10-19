# routes.py

from flask import Blueprint, render_template, request
from app.pico_pubmed import parse_pico_with_cohere, search_pubmed, fetch_pubmed_details, extract_abstracts_from_xml, summarize_paper_with_cohere

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/pico-question', methods=['GET', 'POST'])
def pico_question():
    if request.method == 'POST':
        pico_question = request.form['pico_question']
        
        # Parse the PICO components
        parsed_pico = parse_pico_with_cohere(pico_question)
        
        results = []
        if parsed_pico:
            paper_ids = search_pubmed(parsed_pico)
            if paper_ids:
                paper_details_xml = fetch_pubmed_details(paper_ids)
                if paper_details_xml:
                    abstracts = extract_abstracts_from_xml(paper_details_xml)
                    for abstract in abstracts:
                        summary = summarize_paper_with_cohere(abstract)
                        results.append({
                            'abstract': abstract,
                            'summary': summary
                        })
        
        return render_template('results.html', results=results, pico=parsed_pico)
    
    return render_template('pico_question.html')