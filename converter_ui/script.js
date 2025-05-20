document.getElementById('convertBtn').addEventListener('click', () => {
  const inputText = document.getElementById('inputText').value.trim();
  const resultEl = document.getElementById('result');
  resultEl.textContent = "Загрузка...";

  if (!inputText) {
    resultEl.textContent = "Введите текст для конвертации!";
    return;
  }

  fetch('http://localhost:8000/convert', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: inputText })
  })
  .then(res => {
    if (!res.ok) throw new Error('Ошибка сервера');
    return res.json();
  })
  .then(data => {
    // Предполагается, что ответ в формате { result: "..." }
    resultEl.textContent = JSON.stringify(data, null, 2);
  })
  .catch(err => {
    resultEl.textContent = "Ошибка: " + err.message;
  });
});
