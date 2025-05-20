import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from utils import preprocess_negations

model = pickle.load(open('model/svm_model.pkl', 'rb'))
vectorizer = pickle.load(open('model/vectorizer.pkl', 'rb'))

def predict_with_confidence(text):
    text = preprocess_negations(text)
    vec = vectorizer.transform([text])
    proba = model.predict_proba(vec)[0]
    confidence = sorted(zip(model.classes_, proba), key=lambda x: -x[1])
    return confidence

def train_and_save_model():
    df = pd.read_csv('data/dataset.csv')
    X = df['text']
    y = df['label']

    vectorizer = TfidfVectorizer(stop_words='english')
    X_vec = vectorizer.fit_transform(X)

    model = SVC(probability=True, kernel='linear')
    model.fit(X_vec, y)

    os.makedirs('model', exist_ok=True)
    pickle.dump(model, open('model/svm_model.pkl', 'wb'))
    pickle.dump(vectorizer, open('model/vectorizer.pkl', 'wb'))

if __name__ == "__main__":
    train_and_save_model()
