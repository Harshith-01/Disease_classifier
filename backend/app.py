from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import preprocess_negations
from classifier import predict_with_confidence
from clarifier import get_clarifying_questions

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get("text", "")
    answers = data.get("answers", {})

    processed_text = preprocess_negations(text)
    predictions = predict_with_confidence(processed_text)

    # Adjust predictions with clarification answers
    if answers:
        adjusted_predictions = []
        for disease, conf in predictions:
            clarifiers = get_clarifying_questions([disease]).get(disease, {})
            questions = clarifiers.get("questions", [])
            penalty = 0
            bonus = 0
            for q in questions:
                ans = answers.get(q)
                if ans == "no":
                    penalty += 0.3
                elif ans == "yes":
                    bonus += 0.2
            new_conf = conf + bonus - penalty
            if new_conf > 0:
                adjusted_predictions.append((disease, new_conf))
        if adjusted_predictions:
            predictions = sorted(adjusted_predictions, key=lambda x: -x[1])

    # Trigger clarification if confidence is low
    if len(predictions) > 1 and predictions[0][1] - predictions[1][1] < 0.2:
        top_diseases = [predictions[0][0], predictions[1][0]]
        followup = get_clarifying_questions(top_diseases)
        return jsonify({
            "status": "clarify",
            "predictions": predictions,
            "followup": followup
        })

    return jsonify({
        "status": "final",
        "prediction": predictions[0][0],
        "confidence": round(predictions[0][1], 3)
    })

@app.route('/reset-session', methods=['POST'])
def reset_session():
    return jsonify({"status": "reset successful"})

@app.route('/predefined-symptoms', methods=['GET'])
def predefined_symptoms():
    return jsonify([
        "pain", "rash", "swelling", "itch", "fever", "cough", "fatigue",
        "nausea", "headache", "dizziness", "inflammation", "cramps", "burning",
        "discomfort", "weakness", "chills", "redness", "peeling", "discharge",
        "tenderness", "stiffness", "blisters", "lesions", "ulcers", "spots"
    ])

if __name__ == '__main__':
    app.run(debug=True)
