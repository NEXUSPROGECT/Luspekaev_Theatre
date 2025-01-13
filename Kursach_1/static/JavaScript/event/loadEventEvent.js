// Получение параметра "id" из URL
function getEventIdFromURL() {
    const urlParts = window.location.pathname.split('/');
    const eventId = urlParts[urlParts.length - 1] || null;
    return eventId;
}

const eventId = getEventIdFromURL();

if (!eventId) {
    console.error("ID ивента отсутствует в URL");
} else {
    console.log("ID ивента:", eventId);
    document.addEventListener('DOMContentLoaded', function() {
        fetchEventData(eventId);
    });
}

async function fetchEventData(eventId) {
    const query = `
        query GetEventDetails($id: ID!) {
            events(id: $id) {
                id
                name
                author
                description
                image
                images {
                    image
                }
                actors {
                    role
                    actor {
                        firstName
                        lastName
                        image
                    }
                }
                times {
                    id
                    date
                    availableSeatsCount
                }
            }
        }
    `;

    const variables = { id: eventId };

    try {
        const response = await fetch('/graphql/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query, variables })
        });

        const data = await response.json();
        // Проверка на ошибки GraphQL
        if (data.errors) {
            console.error("GraphQL errors:", data.errors);
            return;
        }

        const event = data?.data?.events?.[0]; // Получаем первое событие из массива events
        if (!event) {
            console.error("Event not found");
            return;
        }
        console.error(event);

        // Обновление данных события
        document.getElementById('event-image').src = `/${event.image}`;
        document.getElementById('event-title').innerText = event.name;
        document.getElementById('event-author').innerText = `Автор: ${event.author}`;
        document.getElementById('about-text').innerText = event.description;

        const slider = document.getElementById('slider');
        event.images.forEach(image => {
            console.log(image)
            const item = document.createElement('div');
            item.className = "flex-none w-full md:w-1/2 lg:w-1/2 p-2";
            const item2 = document.createElement('div');
            item2.className = "border rounded-lg p-4 text-center"
            const sliderImage = document.createElement('img');
            sliderImage.classList.add('w-full', 'h-auto', 'object-contain', 'border', 'rounded-lg', 'cursor-pointer');
            sliderImage.alt = 'slider-image';
            sliderImage.src = `/${image.image}`;
            item2.appendChild(sliderImage);
            item.appendChild(item2);
            slider.appendChild(item);
        });


        const lightboxSlider = document.getElementById('lightbox-slider');

        // Функция для добавления изображений в слайдер

            event.images.forEach((image, index) => {
                const sliderImage = document.createElement('img');
                sliderImage.className = 'w-full h-auto object-contain border rounded-lg';
                sliderImage.src = `/${image.image}`;
                sliderImage.setAttribute('data-index', index); // Добавление атрибута для идентификации

                // Добавляем изображение в слайдер
                lightboxSlider.appendChild(sliderImage);
            });




        // document.title = event.name

        // Обновление секции актеров
        const charactersList = document.getElementById('characters-list');
        event.actors.forEach(actor => {
            const characterElement = document.createElement('div');
            characterElement.classList.add(
                'flex',
                'items-center',
                'bg-white',
                'shadow-md',
                'rounded-lg',
                'overflow-hidden',
                'hover:shadow-lg',
                'transition'
            );
            characterElement.innerHTML = `
                <!-- Левая часть с изображением -->
                <div class="flex-shrink-0">
                    <img src="/${actor.actor.image}" alt="${actor.actor.firstName}" 
                        class="w-32 h-32 md:w-40 md:h-40 object-cover">
                </div>
                <!-- Правая часть с текстом -->
                <div class="p-4">
                    <h3 class="text-xl font-bold text-gray-800">${actor.actor.firstName} ${actor.actor.lastName}</h3>
                    <p class="text-gray-600 mt-2">Роль: ${actor.role}</p>
                </div>
            `;
            charactersList.appendChild(characterElement);
        });

        // Обработка расписания
        const scheduleTable = document.getElementById('schedule-table').getElementsByTagName('tbody')[0];
        timesID = 0;
        event.times.forEach(time => {
            const rawDate = time.date;
            const date = new Date(rawDate);
            const months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"];
            const day = date.getDate();
            const month = months[date.getMonth()];
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');

            const row = scheduleTable.insertRow();
            row.innerHTML = `
                   <td class="px-4 py-2 text-center">${day} ${month}</td>
                   <td class="px-4 py-2">${hours}:${minutes}</td>
                   <td class="px-4 py-2">${event.times[timesID].availableSeatsCount}</td>
                   <td class="px-4 py-2">
                       <a href="/ticket/${event.times[timesID].id}" class="bg-sky-500 text-white py-2 px-4 rounded shadow hover:bg-sky-700 transition rounded-full">Купить</a>
                   </td>
               `;
            timesID++;
        });
    }
    catch (error) {
        console.error('Error fetching data:', error);
    }
}