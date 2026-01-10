import cohere
import os
import json

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Debug print to confirm deployed version
print("===== PICO_PUBMED.PY: Using co.chat() API (Updated 2026) =====")


# =========================
# PICO PARSING
# =========================
def parse_pico_with_cohere(question: str):
    prompt = (
        "Extract the PICO components from the following clinical question.\n"
        "Return ONLY valid JSON with the keys: Population, Intervention, Comparison, Outcome.\n\n"
        f"Question: {question}"
    )

    # CHANGED: co.generate() -> co.chat()
    response = co.chat(
        model="command-a-03-2025",
        message=prompt,  # CHANGED: prompt -> message
        temperature=0
    )

    text = response.text.strip()  # CHANGED: response.generations[0].text -> response.text

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

    # CHANGED: co.generate() -> co.chat()
    response = co.chat(
        model="command-a-03-2025",
        message=prompt,  # CHANGED: prompt -> message
        temperature=0.3
    )

    return response.text.strip()  # CHANGED: response.generations[0].text -> response.text


# =========================
# QUESTION CLASSIFICATION
# =========================
def classify_question(question: str):
    """
    IMPORTANT:
    - command-a-03-2025 does NOT support classify()
    - 'large' is still valid and REQUIRED here
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