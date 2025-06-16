document.getElementById('convertBtn').addEventListener('click', () => {
  const amountInput = document.getElementById('amount');
  const amount = parseFloat(amountInput.value.trim());
  const from = document.getElementById('fromCurrency').value.trim();
  const to = document.getElementById('toCurrency').value.trim();
  const date = document.getElementById('conversionDate').value.trim();
  const resultEl = document.getElementById('result');

  // Валидация
  if (isNaN(amount) || amount <= 0) {
    resultEl.textContent = "Введите корректную сумму!";
    amountInput.focus();
    return;
  }
  if (!from || !to) {
    resultEl.textContent = "Выберите валюты!";
    return;
  }

  resultEl.textContent = "Загрузка...";

  // Формируем URL запроса
  const baseUrl = location.hostname === "localhost" ? "http://localhost:8000" : "";
  let url = `${baseUrl}/currencies/${encodeURIComponent(from)}/${encodeURIComponent(to)}?amount=${encodeURIComponent(amount)}`;
  if (date) {
    url += `&date=${encodeURIComponent(date)}`;
  }

  fetch(url)
    .then(async res => {
      if (!res.ok) {
        try {
          const contentType = res.headers.get("content-type") || "";
          if (contentType.includes("application/json")) {
            const data = await res.json();
            throw new Error(data.error || "Ошибка запроса. Проверьте параметры.");
          } else {
            const text = await res.text();
            throw new Error(text || "Ошибка запроса.");
          }
        } catch {
          throw new Error("Данные по выбранной дате недоступны. Попробуйте другую дату или уберите дату.");
        }
      }
      return res.json();
    })
.then(data => {
  console.log("Ответ сервера:", data);
  if (data.result !== undefined) {
    const formattedAmount = Number(data.amount).toLocaleString("ru-RU", { minimumFractionDigits: 2 });
    const formattedResult = Number(data.result).toLocaleString("ru-RU", { minimumFractionDigits: 2 });
    const usedDate = data.date || "текущую дату";
    resultEl.textContent = `${formattedAmount} ${data.from} = ${formattedResult} ${data.to} на ${usedDate}`;
  } else if (data.error) {
    resultEl.textContent = "Ошибка: " + data.error;
  } else {
    resultEl.textContent = "Неизвестный ответ от сервера.";
  }
})
    .catch(err => {
      console.error("Ошибка при запросе:", err);
      resultEl.textContent = "Ошибка: " + err.message;
    });
});
