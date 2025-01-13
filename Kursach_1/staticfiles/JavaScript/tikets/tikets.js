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
        fetchEventData(eventId)
            .catch((e) => console.error("Error: " + e));
    });
}

async function fetchEventData(eventId) {
    const query = `
        query GetEventDetails($id: ID!) {            
                eventTime(id: $id) {
                    seats{
                      id
                      row
                      number
                      status
                    }
                }
        }
    `;

    const variables = {id: eventId};

    try {
        const response = await fetch('/graphql/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query: query, variables})
        });

        const data = await response.json();
        // Проверка на ошибки GraphQL
        if (data.errors) {
            console.error("GraphQL errors:", data.errors);
            return;
        }

        const event = data?.data?.eventTime?.[0].seats; // Получаем первое событие из массива events
        if (!event) {
            console.error("Event not found");
            return;
        }
        console.log(event);


        window.myEvent = {"event": event}

        setTimeout(() => {
    console.log("tikets.js завершён.");
    document.dispatchEvent(new Event("tiketsComplete"));
}, 1000);

        window.myEvent = {"event": event}



    }
    catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }

}