document.getElementById('convertBtn').addEventListener('click', () => {
  const amount = parseFloat(document.getElementById('amount').value);
  const from = document.getElementById('fromCurrency').value;
  const to = document.getElementById('toCurrency').value;
  const resultEl = document.getElementById('result');

  resultEl.textContent = "Загрузка...";

  if (isNaN(amount) || amount <= 0) {
    resultEl.textContent = "Введите корректную сумму!";
    return;
  }

  fetch('http://localhost:8000/convert', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ from, to, amount })
  })
  .then(res => {
    if (!res.ok) throw new Error('Ошибка сервера');
    return res.json();
  })
  .then(data => {
    if (data.error) {
      resultEl.textContent = "Ошибка: " + data.error;
    } else {
      resultEl.textContent = `${data.amount} ${data.from} = ${data.result} ${data.to}`;
    }
  })
  .catch(err => {
    resultEl.textContent = "Ошибка: " + err.message;
  });
});
