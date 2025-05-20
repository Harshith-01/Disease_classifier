import pickle
import re

# Load model and vectorizer
model = pickle.load(open('backend/model/svm_model.pkl', 'rb'))
vectorizer = pickle.load(open('backend/model/vectorizer.pkl', 'rb'))

def predict_with_confidence(text):
    vec = vectorizer.transform([text])
    proba = model.predict_proba(vec)[0]
    confidence = sorted(zip(model.classes_, proba), key=lambda x: -x[1])
    return confidence

def preprocess_negations(text):
    # Handle common negations
    negation_patterns = [
        r"\bno (\w+)",
        r"\bnot (\w+)",
        r"\bdon't have (\w+)",
        r"\bdont have (\w+)",
        r"\bdoesn't have (\w+)",
        r"\bdoes not have (\w+)",
        r"\bhaven't (\w+)",
        r"\bhadn't (\w+)"
    ]
    for pattern in negation_patterns:
        text = re.sub(pattern, r"NEG_\1", text, flags=re.IGNORECASE)
    return text.lower()
