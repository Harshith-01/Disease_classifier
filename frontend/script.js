async function loadSymptoms() {
  const res = await fetch('http://127.0.0.1:5000/predefined-symptoms');
  const symptoms = await res.json();
  const container = document.getElementById('symptom-list');
  container.innerHTML = '';
  symptoms.forEach(symptom => {
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = symptom;
    checkbox.id = `symptom_${symptom}`;
    const label = document.createElement('label');
    label.htmlFor = checkbox.id;
    label.textContent = symptom;
    container.appendChild(checkbox);
    container.appendChild(label);
    container.appendChild(document.createElement('br'));
  });
}

let userAnswers = {};
let currentClarifyData = null;

function recordAnswer(question, answer) {
  userAnswers[question] = answer;
}

function prepareAnswersForPayload() {
  return { ...userAnswers };
}

async function submitSymptoms() {
  let userText = document.getElementById('symptomText').value.trim();
  const checked = document.querySelectorAll('#symptom-list input[type=checkbox]:checked');
  checked.forEach(c => { userText += ` ${c.value}`; });

  const payload = { text: userText };
  if (Object.keys(userAnswers).length > 0) payload.answers = prepareAnswersForPayload();

  const res = await fetch('http://127.0.0.1:5000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const result = await res.json();
  const display = document.getElementById('response');
  display.innerHTML = '';

  if (result.status === 'final') {
    display.innerHTML = `<strong>Prediction:</strong> ${result.prediction} <br><strong>Confidence:</strong> ${result.confidence.toFixed(2)}`;
    userAnswers = {};
    currentClarifyData = null;
  } else if (result.status === 'clarify') {
    currentClarifyData = result.followup;
    display.innerHTML = `<strong>Top Predictions:</strong><br>${result.predictions.map(p => `${p[0]} (${(p[1]*100).toFixed(1)}%)`).join("<br>")}`;
    display.innerHTML += `<br><br><strong>Please answer the following:</strong><br>`;
    for (const disease in currentClarifyData) {
      currentClarifyData[disease].questions.forEach(q => {
        const div = document.createElement('div');
        div.innerHTML = `${q}
          <button onclick="recordAndSubmit('${q}', 'yes')">Yes</button>
          <button onclick="recordAndSubmit('${q}', 'no')">No</button>`;
        display.appendChild(div);
      });
    }
  }
}

function recordAndSubmit(question, answer) {
  recordAnswer(question, answer);
  submitSymptoms();
}

async function resetSession() {
  await fetch('http://127.0.0.1:5000/reset-session', { method: 'POST' });
  document.getElementById('symptomText').value = '';
  document.getElementById('response').innerHTML = '';
  userAnswers = {};
}

window.onload = loadSymptoms;
