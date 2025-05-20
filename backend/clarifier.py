import re
disease_data = {
    'Psoriasis': {
        'symptoms': ["joint pain", "nail dents", "skin peeling", "scaly rash"],
        'questions': [
            "Do you have joint pain?",
            "Are your nails affected with dents or discoloration?",
            "Is the skin rash flaky or scaly?"
        ]
    },
    'Varicose Veins': {
        'symptoms': ["visible twisted veins", "leg cramps", "leg swelling", "leg heaviness"],
        'questions': [
            "Do you have visible twisted veins on your legs?",
            "Are you experiencing leg cramps or swelling?",
            "Do your legs feel heavy after standing long?"
        ]
    },
    'Typhoid': {
        'symptoms': ["high fever", "abdominal pain", "constipation", "diarrhea", "rash"],
        'questions': [
            "Are you experiencing a high fever?",
            "Do you have abdominal discomfort?",
            "Have you noticed any changes in bowel movements?",
            "Is there a rose-colored rash on your abdomen?"
        ]
    },
    'Chicken Pox': {
        'symptoms': ["itchy rash", "blisters", "fever", "fatigue"],
        'questions': [
            "Do you have an itchy rash with blisters?",
            "Are the blisters filled with clear fluid?",
            "Have you experienced a recent fever?"
        ]
    },
    'Impetigo': {
        'symptoms': ["red sores", "honey-colored crust", "itching"],
        'questions': [
            "Are there red sores around your nose or mouth?",
            "Do the sores rupture and form a honey-colored crust?",
            "Is the affected area itchy?"
        ]
    },
    'Dengue': {
        'symptoms': ["high fever", "headache", "muscle pain", "rash", "nausea"],
        'questions': [
            "Are you experiencing a high fever?",
            "Do you have severe headaches or pain behind the eyes?",
            "Are you feeling muscle or joint pain?",
            "Have you noticed any skin rash?"
        ]
    },
    'Fungal Infection': {
        'symptoms': ["itchy skin", "redness", "scaly patches", "cracked skin"],
        'questions': [
            "Is your skin itchy or red?",
            "Do you have scaly or cracked skin patches?",
            "Is there any discharge or unpleasant odor?"
        ]
    },
    'Common Cold': {
        'symptoms': ["sore throat", "runny nose", "cough", "sneezing", "fatigue"],
        'questions': [
            "Do you have a sore throat or runny nose?",
            "Are you experiencing frequent sneezing or coughing?",
            "Do you feel fatigued or have mild body aches?"
        ]
    },
    'Pneumonia': {
        'symptoms': ["cough with mucus", "fever", "chills", "shortness of breath"],
        'questions': [
            "Are you coughing up greenish or yellow mucus?",
            "Do you have a high fever or chills?",
            "Are you experiencing shortness of breath?"
        ]
    },
    'Dimorphic Hemorrhoids': {
        'symptoms': ["rectal bleeding", "pain during bowel movements", "itching"],
        'questions': [
            "Have you noticed blood during bowel movements?",
            "Is there pain or discomfort in the anal area?",
            "Do you experience itching around the rectum?"
        ]
    },
    'Arthritis': {
        'symptoms': ["joint pain", "stiffness", "swelling", "reduced mobility"],
        'questions': [
            "Are you experiencing joint pain or stiffness?",
            "Is there swelling in your joints?",
            "Do you find it difficult to move certain joints?"
        ]
    },
    'Acne': {
        'symptoms': ["pimples", "blackheads", "whiteheads", "oily skin"],
        'questions': [
            "Do you have pimples or blackheads on your face or body?",
            "Is your skin oily or prone to breakouts?",
            "Are there any inflamed or painful skin lesions?"
        ]
    },
    'Bronchial Asthma': {
        'symptoms': ["wheezing", "shortness of breath", "chest tightness", "coughing"],
        'questions': [
            "Do you experience wheezing or shortness of breath?",
            "Is there a tight feeling in your chest?",
            "Do you have frequent coughing, especially at night?"
        ]
    },
    'Hypertension': {
        'symptoms': ["headaches", "dizziness", "blurred vision", "nosebleeds"],
        'questions': [
            "Have you experienced frequent headaches or dizziness?",
            "Is your vision sometimes blurred?",
            "Do you have occasional nosebleeds?"
        ]
    },
    'Migraine': {
        'symptoms': ["throbbing headache", "nausea", "sensitivity to light", "visual disturbances"],
        'questions': [
            "Do you have throbbing headaches on one side of your head?",
            "Are you sensitive to light or sound during headaches?",
            "Do you experience nausea or visual auras?"
        ]
    },
    'Cervical Spondylosis': {
        'symptoms': ["neck pain", "stiffness", "headaches", "shoulder pain"],
        'questions': [
            "Do you have persistent neck pain or stiffness?",
            "Are you experiencing headaches originating from the neck?",
            "Is there pain radiating to your shoulders or arms?"
        ]
    },
    'Jaundice': {
        'symptoms': ["yellowing of skin", "dark urine", "fatigue", "abdominal pain"],
        'questions': [
            "Is your skin or the whites of your eyes yellowing?",
            "Have you noticed dark-colored urine?",
            "Are you feeling unusually tired or experiencing abdominal discomfort?"
        ]
    },
    'Malaria': {
        'symptoms': ["fever", "chills", "sweating", "headache", "nausea"],
        'questions': [
            "Do you have recurring fevers with chills and sweating?",
            "Are you experiencing headaches or nausea?",
            "Have you recently traveled to a malaria-prone area?"
        ]
    },
    'Urinary Tract Infection': {
        'symptoms': ["burning sensation during urination", "frequent urination", "cloudy urine", "pelvic pain"],
        'questions': [
            "Do you feel a burning sensation while urinating?",
            "Are you urinating more frequently than usual?",
            "Is your urine cloudy or has a strong odor?"
        ]
    },
    'Allergy': {
        'symptoms': ["sneezing", "itchy eyes", "runny nose", "skin rash"],
        'questions': [
            "Are you experiencing sneezing or a runny nose?",
            "Do you have itchy or watery eyes?",
            "Is there any skin rash or hives?"
        ]
    },
    'Gastroesophageal Reflux Disease': {
        'symptoms': ["heartburn", "acid reflux", "chest pain", "difficulty swallowing"],
        'questions': [
            "Do you have frequent heartburn or acid reflux?",
            "Is there a sour taste in your mouth?",
            "Do you experience chest pain or difficulty swallowing?"
        ]
    },
    'Drug Reaction': {
        'symptoms': ["skin rash", "fever", "itching", "swelling"],
        'questions': [
            "Have you developed a skin rash after taking medication?",
            "Are you experiencing itching or swelling?",
            "Do you have a fever without other symptoms?"
        ]
    },
    'Peptic Ulcer Disease': {
        'symptoms': ["abdominal pain", "bloating", "nausea", "heartburn"],
        'questions': [
            "Do you have burning abdominal pain, especially when hungry?",
            "Are you experiencing bloating or nausea?",
            "Is there relief after eating or taking antacids?"
        ]
    },
    'Diabetes': {
        'symptoms': ["frequent urination", "increased thirst", "unexplained weight loss", "fatigue"],
        'questions': [
            "Are you urinating more frequently than usual?",
            "Do you feel excessively thirsty?",
            "Have you experienced unexplained weight loss or fatigue?"
        ]
    }
}


def normalize_symptom(symptom):
    """Normalize symptom text for consistent matching."""
    return re.sub(r'\s+', ' ', symptom.strip().lower())


def get_clarifying_questions(possible_diseases, confirmed_symptoms=None):
    """
    Returns relevant clarification questions for possible diseases,
    excluding confirmed symptoms if provided.
    """
    confirmed_set = set(normalize_symptom(sym) for sym in confirmed_symptoms) if confirmed_symptoms else set()
    result = {}

    for disease in possible_diseases:
        if disease not in disease_data:
            continue

        disease_info = disease_data[disease]
        filtered_questions = []
        for symptom, question in zip(disease_info['symptoms'], disease_info['questions']):
            if normalize_symptom(symptom) not in confirmed_set:
                filtered_questions.append(question)

        result[disease] = {
            "symptoms": [normalize_symptom(s) for s in disease_info['symptoms']],
            "questions": filtered_questions
        }

    return result

def adjust_confidence(conf, questions, answers):
    question_count = len(questions)
    weight = 0.2 / question_count
    bonus = 0.0
    penalty = 0.0

    for q in questions:
        ans = answers.get(q, "").strip().lower()
        if ans == "yes":
            bonus += weight
        elif ans == "no":
            penalty += weight

    new_conf = max(0, min(conf + bonus - penalty, 1.0))
    return new_conf

