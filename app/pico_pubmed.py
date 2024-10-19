# pico_pubmed.py

import cohere
import requests
import json
import xml.etree.ElementTree as ET

# Initialize Cohere client
co = cohere.Client('IguNqlbuOavI0k4CWMEumaQXUm3OQjDMmLa2P4ju')

def parse_pico_with_cohere(question):
    prompt = f"Extract the PICO components (Patient, Intervention, Comparison, Outcome) from the following question: \n\n'{question}'"
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
    patient = pico_components.get('Patient', '')
    intervention = pico_components.get('Intervention', '')
    comparison = pico_components.get('Comparison', '')
    outcome = pico_components.get('Outcome', '')
    term = f"{patient} AND {intervention} AND {comparison} AND {outcome}"
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
    abstracts = []
    for article in root.findall(".//PubmedArticle"):
        abstract = article.find(".//AbstractText")
        if abstract is not None:
            abstracts.append(abstract.text)
    return abstracts

def summarize_paper_with_cohere(paper_abstract):
    prompt = f"Summarize the following research abstract in 2-3 sentences:\n\n'{paper_abstract}'"
    response = co.chat(
        model='command-r',
        message=prompt,
    )
    return response.text