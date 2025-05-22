document.getElementById('convertBtn').addEventListener('click', () => {
  const amountInput = document.getElementById('amount');
  const amount = parseFloat(amountInput.value);
  const from = document.getElementById('fromCurrency').value;
  const to = document.getElementById('toCurrency').value;
  const resultEl = document.getElementById('result');

  if (isNaN(amount) || amount <= 0) {
    resultEl.textContent = "Введите корректную сумму!";
    amountInput.focus();
    return;
  }

  resultEl.textContent = "Загрузка...";

  const url = `http://localhost:8000/currencies/${encodeURIComponent(from)}/${encodeURIComponent(to)}?amount=${encodeURIComponent(amount)}`;

  fetch(url)
    .then(res => {
      if (!res.ok) {
        return res.text().then(text => { throw new Error(text || 'Ошибка сервера'); });
      }
      return res.json();
    })
    .then(data => {
      console.log('Ответ от сервера:', data); // Для отладки

      if (data.result !== undefined) {
        resultEl.textContent = `${data.amount} ${data.from} = ${data.result} ${data.to}`;
      } else if (data.error) {
        resultEl.textContent = "Ошибка: " + data.error;
      } else {
        resultEl.textContent = "Неизвестный ответ от сервера";
      }
    })
    .catch(err => {
      console.error('Ошибка в fetch:', err);
      resultEl.textContent = "Ошибка: " + err.message;
    });
});
