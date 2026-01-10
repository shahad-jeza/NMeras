# pico_search.py

import os
import json
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import cohere

# --------------------------------------------------
# Setup
# --------------------------------------------------

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

COHERE_CHAT_MODEL = "command"  # ✅ ONLY supported stable chat model

# --------------------------------------------------
# Question Classification
# --------------------------------------------------

def classify_question(question):
    """
    Classifies a given question as either Case 1 or Case 2 using Cohere.
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

    examples = (
        [{"text": ex, "label": "case1"} for ex in case1_examples] +
        [{"text": ex, "label": "case2"} for ex in case2_examples]
    )

    response = co.classify(
        inputs=[question],
        examples=examples,
        model="large"
    )

    return response.classifications[0].prediction


# --------------------------------------------------
# PICO Parsing (FIXED)
# --------------------------------------------------

def parse_pico_with_cohere(question):
    prompt = (
        "Extract the PICO components from the following question.\n"
        "Return ONLY valid JSON with these keys:\n"
        "Patient, Intervention, Comparison, Outcome\n\n"
        f"{question}"
    )

    response = co.chat(
        model=COHERE_CHAT_MODEL,
        message=prompt
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "Patient": "",
            "Intervention": "",
            "Comparison": "",
            "Outcome": ""
        }


# --------------------------------------------------
# PubMed Search
# --------------------------------------------------

def search_pubmed(pico_components):
    if not pico_components:
        return []

    patient = pico_components.get("Patient", "")
    intervention = pico_components.get("Intervention", "")
    comparison = pico_components.get("Comparison", "")
    outcome = pico_components.get("Outcome", "")

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
        return response.json()["esearchresult"]["idlist"]

    return []


def fetch_pubmed_details(paper_ids):
    if not paper_ids:
        return None

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml",
        "rettype": "abstract"
    }

    response = requests.get(base_url, params=params)
    return response.text if response.status_code == 200 else None


def extract_abstracts_from_xml(xml_data):
    root = ET.fromstring(xml_data)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", default="No Title")
        abstract = article.find(".//AbstractText")
        pmid = article.findtext(".//PMID", default="")

        if abstract is not None:
            articles.append({
                "title": title,
                "abstract": abstract.text,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}"
            })

    return articles


# --------------------------------------------------
# Paper Summarization (FIXED)
# --------------------------------------------------

def summarize_paper_with_cohere(paper_abstract):
    prompt = (
        "Summarize the following research abstract in 2–3 concise sentences:\n\n"
        f"{paper_abstract}"
    )

    response = co.chat(
        model=COHERE_CHAT_MODEL,
        message=prompt
    )

    return response.text