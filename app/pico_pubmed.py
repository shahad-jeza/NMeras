# pico_search.py
import cohere
import requests
import json
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Initialize Cohere client
co = cohere.Client(os.getenv('COHERE_API_KEY'))

import cohere

import cohere

def classify_question(question):
    """
    Classifies a given question as either Case 1 or Case 2 using Cohere.
    
    Case 1: In [population], does [intervention] improve [outcome] compared to [comparison]?
    Case 2: In [population], does [intervention] reduce the incidence of [outcome] compared to [comparison]?
    
    Parameters:
    question (str): The question to be classified.
    
    Returns:
    str: 'case1' if the question matches Case 1, 'case2' if the question matches Case 2, 'unknown' otherwise.
    """

    case1_examples = [
        "In pediatric patients with type 1 diabetes, does continuous glucose monitoring improve glycemic control compared to traditional fingerstick monitoring?",
        "Does continuous glucose monitoring enhance glycemic control in pediatric type 1 diabetes patients compared to traditional fingerstick monitoring?",
        "For patients with pediatric type 1 diabetes, is continuous glucose monitoring better than traditional fingerstick monitoring for improving glycemic control?"
    ]

    case2_examples = [
        "In bedridden patients, does the use of air mattress reduce the incidence of pressure ulcers compared to other method?",
        "Does air mattress decrease pressure ulcers in bedridden patients compared to other methods?",
        "For bedridden patients, does air mattress lower the risk of pressure ulcers compared to other methods?"
    ]

    examples = [
        {"text": ex, "label": "case1"} for ex in case1_examples
    ] + [
        {"text": ex, "label": "case2"} for ex in case2_examples
    ]

    # Make a prediction
    response = co.classify(
        inputs=[question],
        examples=examples,
        model='large',  # Adjust model if needed
    )

    # Get the predicted label
    prediction = response.classifications[0].prediction

    return prediction


# Summarize each abstract using Cohere API
def summarize_abstracts():
    summaries = []
    for paper in abstracts_and_scores_sorted:
        prompt = (
            f"Summarize the following medical research abstract carefully. "
            f"Preserve important terminology and concepts, and ensure accuracy for any details about the patient type, "
            f"such as whether they are a child, adult, or elderly:\n\n"
            f"{paper['abstract']}"
        )
        response = co.summarize(text=prompt, length="medium", model="cohere-summarize")
        summary = response.summary if response else "Summary not available."
        summaries.append({"title": paper["title"], "summary": summary, "score": paper["score"]})
    return summaries






    #-------------------------------------#
def parse_pico_with_cohere(question):
    prompt = f"Extract the PICO components (Patient, Intervention, Comparison, Outcome) from the following question, please write it in the correct order: \n\n'{question}'"
    response = co.chat(
        model='command-r',
        message=prompt,
        response_format={"type": "json_object"}
    )
    print("Raw response from Cohere:", response.text)
    try:
        parsed_response = json.loads(response.text)
        print("Parsed JSON response:", parsed_response)
        return parsed_response
    except json.JSONDecodeError:
        print("Error: Unable to parse PICO components. Invalid JSON format.")
        return None

def search_pubmed(pico_components):
    if not pico_components:
        print("No valid PICO components found.")
        return []
    
    # Create a combined search term emphasizing systematic reviews
    patient = pico_components.get('Patient', '')
    intervention = pico_components.get('Intervention', '')
    comparison = pico_components.get('Comparison', '')
    outcome = pico_components.get('Outcome', '')
    term = f"({patient} OR {intervention} OR {comparison} OR {outcome}) AND systematic review"
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "retmax": 5
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        search_results = response.json()
        return search_results['esearchresult']['idlist']
    else:
        print(f"Error: PubMed search failed with status code {response.status_code}")
        return []

def fetch_pubmed_details(paper_ids):
    if not paper_ids:
        print("No paper IDs provided.")
        return None
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml",
        "rettype": "abstract"
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Failed to fetch paper details with status code {response.status_code}")
        return None

def extract_abstracts_from_xml(xml_data):
    root = ET.fromstring(xml_data)
    articles = []
    for article in root.findall(".//PubmedArticle"):
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No Title"
        abstract = article.find(".//AbstractText")
        url = f"https://pubmed.ncbi.nlm.nih.gov/{article.find('.//PMID').text}" if article.find(".//PMID") is not None else ""
        
        if abstract is not None:
            articles.append({
                'title': title,
                'abstract': abstract.text,
                'url': url
            })
    return articles

def summarize_paper_with_cohere(paper_abstract):
    prompt = f"Summarize the following research abstract in 2-3 sentences:\n\n'{paper_abstract}'"
    response = co.chat(
        model='command-r',
        message=prompt,
    )
    return response.text