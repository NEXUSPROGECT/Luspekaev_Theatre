// Функция для загрузки данных и рендеринга
async function fetchAndRenderData() {
  const query = `
    query {
      eventImportant {
        id
        name
        description
        image
        event {
          id
        }
      }
      events {
        id
        name
        type
        description
        image
        times {
          date
          availableSeatsCount
        }
      }
    }
  `;

  try {
    // Выполняем запрос
    const response = await fetch('/graphql/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });

    const result = await response.json();
    console.log("Результат GraphQL-запроса:", result);

    // Рендерим данные для eventImportant
    renderImportantEvents(result.data.eventImportant || [], 'sliderEvents');

    // Рендерим данные для events с общей сортировкой по дате
    renderSortedEvents(result.data.events || [], 'slider');
  } catch (error) {
    console.error("Ошибка при выполнении запросов:", error);
  }
}

// Функция рендеринга важных событий
function renderImportantEvents(events, containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = ''; // Очищаем контейнер

  events.forEach(event => {
    const item = document.createElement('div');
    item.className = "w-full flex-none bg-cover bg-center h-[600px]";
    item.style.backgroundImage = `url('/${event.image}')`;

    item.innerHTML = `
      <div class="flex flex-col justify-center items-center text-center h-full bg-black bg-opacity-50 p-4 sm:p-16">
        <h2 class="text-white text-4xl font-bold mb-4">${event.name}</h2>
        <h3 class="text-white text-sm sm:text-xl font-bold mb-4 max-w-[80%] sm:max-w-[60%]">${event.description}</h3>
        <a href="/event/${event.event.id}" class="px-6 py-2 bg-sky-500 text-white rounded-full hover:bg-sky-600">Подробнее</a>
      </div>
    `;

    container.appendChild(item);
  });
}

// Функция рендеринга отсортированных событий
function renderSortedEvents(events, containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = ''; // Очищаем контейнер

  // Собираем все события с их датами в единый массив
  const allEvents = events.flatMap(event =>
    event.times.map(time => ({
      id: event.id,
      name: event.name,
      type: event.type,
      description: event.description,
      image: event.image,
      date: time.date,
      availableSeatsCount: time.availableSeatsCount,
    }))
  );

  // Сортируем события по дате
  allEvents.sort((a, b) => new Date(a.date) - new Date(b.date));

  // Рендерим каждое событие
  allEvents.forEach(event => {
    const item = document.createElement('div');
    item.className = "flex-none w-full md:w-1/2 lg:w-1/3 px-2";

    // Преобразуем дату
    const date = new Date(event.date);
    const months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"];
    const day = date.getDate();
    const month = months[date.getMonth()];
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    item.innerHTML = `
      <div class="bg-white shadow-lg rounded-lg p-4 text-center mt-3">
        <p class="text-gray-600">${day} ${month}<br>${hours}:${minutes}</p>
        <a href="/event/${event.id}" target="_blank">
          <div class="h-32 w-full bg-gray-200 mb-4 rounded-lg bg-cover bg-center" style="background-image: url('/${event.image}');"></div>
        </a>
        <p class="text-sm text-gray-500">${event.type}</p>
        <h3 class="text-xl text-sky-500 font-bold">${event.name}</h3>
        <div class="flex items-center justify-between mt-4">
          <p class="text-sm text-gray-500 text-center">Доступно билетов: ${event.availableSeatsCount}</p>
          <a href="/event/${event.id}#schedule-tickets" class="px-4 py-2 bg-sky-500 text-white rounded-lg hover:bg-blue-700">Билеты</a>
        </div>
      </div>
    `;
    container.appendChild(item);
  });
}

// Загружаем данные после загрузки страницы
document.addEventListener('DOMContentLoaded', fetchAndRenderData);
