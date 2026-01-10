import cohere
import os
import json

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))


# =========================
# PICO PARSING
# =========================
def parse_pico_with_cohere(question: str):
    prompt = (
        "Extract the PICO components from the following clinical question.\n"
        "Return ONLY valid JSON with the keys: Population, Intervention, Comparison, Outcome.\n\n"
        f"Question: {question}"
    )

    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0
    )

    text = response.text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Safe fallback (prevents app crash)
        return {
            "Population": "",
            "Intervention": "",
            "Comparison": "",
            "Outcome": ""
        }


# =========================
# ARTICLE SUMMARIZATION
# =========================
def summarize_paper_with_cohere(abstract: str):
    prompt = (
        "Summarize the following medical abstract in 2–3 concise sentences:\n\n"
        f"{abstract}"
    )

    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0.3
    )

    return response.text.strip()


# =========================
# QUESTION CLASSIFICATION
# =========================
def classify_question(question: str):
    """
    Note: The classify endpoint is still working for now,
    but consider migrating to chat for classification too.
    """
    examples = [
        {
            "text": "Does drug A reduce blood pressure compared to drug B?",
            "label": "case1"
        },
        {
            "text": "What is the effectiveness of intervention X in elderly patients?",
            "label": "case2"
        }
    ]

    response = co.classify(
        model="large",
        inputs=[question],
        examples=examples
    )

    return response.classifications[0].prediction