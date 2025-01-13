def populate_seats(event_id, seats_matrix):
    from .models import Seat, EventTime  # Подставьте название вашего приложения
    event_time = EventTime.objects.get(id=event_id)
    for row_number, seat_count in enumerate(seats_matrix, start=1):
        for seat_number in range(1, seat_count + 1):
            Seat.objects.create(row=row_number, number=seat_number, event_time=event_time)