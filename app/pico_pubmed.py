import cohere
import os
import json

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Debug print to confirm deployed version
print("===== PICO_PUBMED.PY: Fully updated for Cohere Chat API =====")


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
# QUESTION CLASSIFICATION (UPDATED FOR CHAT API)
# =========================
def classify_question(question: str):
    """
    UPDATED: Migrated from co.classify() to co.chat() for classification
    Classify questions as 'case1' or 'case2' using the Chat API
    """
    
    # Define examples for the model
    system_prompt = """You are a medical question classifier. Classify the following clinical question as either 'case1' or 'case2'.
    
    Examples:
    1. "Does drug A reduce blood pressure compared to drug B?" → case1
    2. "What is the effectiveness of intervention X in elderly patients?" → case2
    3. "In patients with diabetes, does medication Y improve outcomes compared to placebo?" → case1
    4. "How effective is therapy Z for treating depression in adolescents?" → case2
    
    Return ONLY the classification label: either 'case1' or 'case2'."""
    
    prompt = f"Classify this question: {question}"
    
    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0,
        preamble=system_prompt
    )
    
    # Extract classification from response
    result = response.text.strip().lower()
    
    # Clean up the response to ensure we get only case1 or case2
    if 'case1' in result:
        return 'case1'
    elif 'case2' in result:
        return 'case2'
    else:
        # Default fallback
        return 'case1'


# Alternative simpler version if above doesn't work:
def classify_question_simple(question: str):
    """
    Simpler version of classification using direct prompt
    """
    prompt = f"""Classify this medical question as 'case1' or 'case2':
    
    Question: {question}
    
    Return ONLY one word: either 'case1' or 'case2'.
    
    case1 questions typically compare interventions (e.g., "Does A work better than B?").
    case2 questions typically ask about effectiveness of a single intervention."""
    
    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0,
        max_tokens=10  # Limit response to just the classification
    )
    
    result = response.text.strip().lower()
    
    # Clean and validate response
    if 'case1' in result:
        return 'case1'
    elif 'case2' in result:
        return 'case2'
    else:
        # If unclear, default to case1
        return 'case1'