function showAlert(message, backgroundColor = "#ff4d4d") {
  const alertBox = document.getElementById("custom-alert");
  const alertMessage = document.getElementById("alert-message");

  // Устанавливаем текст сообщения
  alertMessage.textContent = message;

  // Применяем цвет фона, если передан
  alertBox.style.backgroundColor = backgroundColor;

  // Показываем алерт, сдвигаем его вверх
  alertBox.classList.remove("hidden");
  setTimeout(() => {
    alertBox.style.bottom = "20px";
  }, 0);

  // Скрываем алерт через 3 секунды
  setTimeout(() => {
    alertBox.style.bottom = "-100px";
    setTimeout(() => alertBox.classList.add("hidden"), 500);
  }, 3000);
}