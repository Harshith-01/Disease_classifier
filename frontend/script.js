async function loadSymptoms() {
  const res = await fetch('http://127.0.0.1:5000/predefined-symptoms');
  const symptoms = await res.json();
  const container = document.getElementById('symptom-list');
  container.innerHTML = '';

  symptoms.forEach(symptom => {
    const wrapper = document.createElement('div');
    wrapper.className = "flex items-center space-x-2";

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = symptom;
    checkbox.id = `symptom_${symptom}`;
    checkbox.className = "form-checkbox h-4 w-4 text-indigo-600";

    const label = document.createElement('label');
    label.htmlFor = checkbox.id;
    label.textContent = symptom;
    label.className = "text-sm";

    wrapper.appendChild(checkbox);
    wrapper.appendChild(label);
    container.appendChild(wrapper);
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
    display.innerHTML = `
      <div class="bg-green-100 p-4 rounded-xl shadow-md">
        <p class="text-lg font-semibold text-green-700">🩺 Final Prediction:</p>
        <p><strong>Disease:</strong> ${result.prediction}</p>
        <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%</p>
      </div>
    `;
    userAnswers = {};
    currentClarifyData = null;
  } else if (result.status === 'clarify') {
    currentClarifyData = result.followup;
    display.innerHTML = `
      <div class="bg-yellow-100 p-4 rounded-xl shadow-md space-y-2">
        <p class="text-lg font-semibold text-yellow-800">🤖 Need Clarification:</p>
        <p><strong>Top Predictions:</strong></p>
        <ul class="list-disc ml-5">${result.predictions.map(p => `<li>${p[0]} (${(p[1] * 100).toFixed(1)}%)</li>`).join("")}</ul>
        <p class="mt-2">Please answer the following questions:</p>
      </div>
    `;

    for (const disease in currentClarifyData) {
      currentClarifyData[disease].questions.forEach(q => {
        const div = document.createElement('div');
        div.className = "mt-2 bg-white p-3 rounded-lg shadow flex justify-between items-center";
        div.innerHTML = `
          <span class="text-gray-700">${q}</span>
          <div class="space-x-2">
            <button onclick="recordAndSubmit('${q}', 'yes')" class="px-3 py-1 bg-blue-500 text-white rounded">Yes</button>
            <button onclick="recordAndSubmit('${q}', 'no')" class="px-3 py-1 bg-red-500 text-white rounded">No</button>
          </div>
        `;
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
