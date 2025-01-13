document.addEventListener("tiketsComplete", () => {
    // Исходные данные
    const hall = document.getElementById("hall");
    const seatMargin = 5; // Отступ между местами
    const rowMargin = 20; // Отступ между рядами
    let seatSize = 30; // Размер места, будет динамически изменяться

    function calculateSeatSize(matrix) {
        if (!hall) return 30;
        const containerWidth = hall.getBoundingClientRect().width;
        const maxSeatsInRow = Math.max(...matrix.map(row => row.length));
        return Math.max(10, (containerWidth - seatMargin * maxSeatsInRow) / maxSeatsInRow);
    }

    function drawSeats(matrix) {
        if (!hall) return;

        // Вычисление размеров SVG
        seatSize = calculateSeatSize(matrix);
        const svgHeight = matrix.length * (seatSize + rowMargin) + seatSize * 2; // Увеличение высоты под сцену
        const svgWidth = hall.getBoundingClientRect().width;

        hall.setAttribute("viewBox", `0 0 ${svgWidth} ${svgHeight}`);
        hall.innerHTML = ""; // Очистка перед перерисовкой

        let yOffset = rowMargin; // Начальная позиция по оси Y

        // Отрисовка мест
        matrix.forEach((row, rowIndex) => {
            const rowWidth = row.length * (seatSize + seatMargin) - seatMargin;
            let xOffset = (svgWidth - rowWidth) / 2; // Центрирование ряда

            row.forEach(seatItem => {
                // Создание места
                const seat = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                seat.setAttribute("x", xOffset.toString());
                seat.setAttribute("y", yOffset.toString());
                seat.setAttribute("width", seatSize.toString());
                seat.setAttribute("height", seatSize.toString());
                seat.setAttribute("class", "seat");
                seat.setAttribute("data-row", seatItem.row + 1);
                seat.setAttribute("data-seat", seatItem.number + 1);
                seat.setAttribute("data-id", seatItem.id);

                // Установка цвета в зависимости от статуса места
                switch (seatItem.status) {
                    case "AVAILABLE":
                        seat.setAttribute("fill", "green");
                        seat.setAttribute("data-clicked", "false");
                        break;
                    case "BOOKED":
                        seat.setAttribute("fill", "gray");
                        seat.setAttribute("data-clicked", "unavailable");
                        break;
                    case "SELECTED":
                        seat.setAttribute("fill", "red");
                        seat.setAttribute("data-clicked", "true");
                        break;
                }

                // Обработчик клика
                seat.addEventListener("click", () => toggleSeat(seat));

                // Добавление в SVG
                hall.appendChild(seat);

                // Добавление номера места
                const seatNumber = document.createElementNS("http://www.w3.org/2000/svg", "text");
                seatNumber.setAttribute("x", (xOffset + seatSize / 2).toString());
                seatNumber.setAttribute("y", (yOffset + seatSize / 2).toString());
                seatNumber.setAttribute("text-anchor", "middle");
                seatNumber.setAttribute("dominant-baseline", "middle");
                seatNumber.setAttribute("font-size", (seatSize / 2.5).toString());
                seatNumber.textContent = `${seatItem.row}-${seatItem.number}`;
                hall.appendChild(seatNumber);

                xOffset += seatSize + seatMargin; // Смещение по X
            });

            yOffset += seatSize + rowMargin; // Смещение по Y для следующего ряда
        });

        // Добавление сцены
        const stageHeight = seatSize;
        const stageYOffset = yOffset + rowMargin; // Позиция сцены ниже всех мест
        const stage = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        stage.setAttribute("x", "0");
        stage.setAttribute("y", stageYOffset.toString());
        stage.setAttribute("width", svgWidth.toString());
        stage.setAttribute("height", stageHeight.toString());
        stage.setAttribute("fill", "#ccc");
        hall.appendChild(stage);

        const stageText = document.createElementNS("http://www.w3.org/2000/svg", "text");
        stageText.setAttribute("x", (svgWidth / 2).toString());
        stageText.setAttribute("y", (stageYOffset + stageHeight / 2).toString());
        stageText.setAttribute("text-anchor", "middle");
        stageText.setAttribute("dominant-baseline", "middle");
        stageText.setAttribute("font-size", (seatSize / 2).toString());
        stageText.textContent = "Сцена";
        hall.appendChild(stageText);
    }


    function toggleSeat(seat) {
        const isClicked = seat.getAttribute("data-clicked");
        if (isClicked === "true") {
            seat.setAttribute("fill", "green");
            seat.setAttribute("data-clicked", "false");
            console.log(seat)
        } else if (isClicked === "false") {
            seat.setAttribute("fill", "red");
            seat.setAttribute("data-clicked", "true");
            console.log(seat)
        }
    }

    function initialize() {

        // Предполагается, что `window.myEvent.event` содержит данные о местах
        const groupedSeats = groupSeatsByRows(window.myEvent.event);
        drawSeats(groupedSeats);
    }

    function groupSeatsByRows(eventData) {
        const rows = {};
        eventData.forEach(seat => {
            if (!rows[seat.row]) {
                rows[seat.row] = [];
            }
            rows[seat.row].push(seat);
        });
        return Object.values(rows);
    }

    // Инициализация схемы и обработчик изменения размера окна
    window.addEventListener("resize", initialize);
    initialize();


    document.getElementById('buttonBuy').addEventListener('click', createTickets);

});








function createTickets() {
// Собираем все выбранные места
    const selectedSeats = [];
    const allSeats = document.querySelectorAll(".seat");

    allSeats.forEach(seat => {
        if (seat.getAttribute("data-clicked") === "true") {
            const seatId = seat.getAttribute("data-id");  // Предполагается, что в аттрибуте "data-id" хранится ID места
            selectedSeats.push(seatId);
        }
    });

    if (selectedSeats.length === 0) {
        showAlert("Выберите хотя бы одно место");

        return;
    }

    // Отправляем запрос GraphQL на сервер
    createTicketsGraphQL(selectedSeats);
}

function createTicketsGraphQL(selectedSeats) {
    // Получаем ID пользователя (предположим, что это доступно на стороне клиента)

    try {
        if (userId === null) {
        return;
        }

    }
    catch (e) {
        window.location.assign("/users/account/login/");
    }


    // Формируем запрос GraphQL
    const mutation = `
        mutation {
            createTickets(userId: "${userId}", seatIds: [${selectedSeats.map(id => `"${id}"`).join(", ")}]) {
                tickets {
                    id
                    seat {
                        id
                        row
                        number
                    }
                    purchaseDate
                }
            }
        }
    `;

    // Отправка запроса через fetch
    fetch('/graphql/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: mutation })
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            console.error("Error creating tickets:", data.errors);
        } else {
            console.log("Tickets created successfully:", data.data.createTickets.tickets);
            // Обработка успешного ответа, например, отображение информации о билете
            showAlert("Билеты добавлены в ваш профиль!", "#7DDA58");
            setTimeout(() => {
                window.location.href = "/users/account/profile/";
            }, 3000);

        }
    })
    .catch(error => {
        console.error("Error during GraphQL request:", error);
    });
}

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
