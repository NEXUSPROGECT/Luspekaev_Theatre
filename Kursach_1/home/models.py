from django.db import models
from django.utils.timezone import localtime
from nanoid import generate

def generate_nanoid():
    return generate(size=10)


class Events(models.Model):
    id = models.CharField(primary_key=True, max_length=10, default=generate_nanoid, editable=False)
    name = models.CharField(max_length=50, unique=True, null=False)
    author = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='static/events/main_image/', null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class EventImage(models.Model):
    id = models.CharField(
        primary_key=True, max_length=10, default=generate_nanoid, editable=False
    )
    event = models.ForeignKey(
        Events, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="static/event_images/")

    def __str__(self):
        return f"Image for {self.event.name}"

class EventTime(models.Model):
    id = models.CharField(primary_key=True, max_length=10, default=generate_nanoid, editable=False)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.event.name} on {self.date.strftime('%Y-%m-%d %H:%M')}"

    @property
    def weekday(self):
        # Использует локализованное время для корректного отображения
        return localtime(self.date).strftime('%A')


class EventImportant(models.Model):
    id = models.CharField(
        primary_key=True, max_length=10, default=generate_nanoid, editable=False
    )
    event = models.OneToOneField(
        Events, on_delete=models.CASCADE, related_name="important", verbose_name="Event"
    )

    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to="static/events/main_events", null=True, blank=True)


    class Meta:
        verbose_name = "Important Event"
        verbose_name_plural = "Important Events"

    def __str__(self):
        return f"Important: {self.event.name}"



class Actors(models.Model):
    id = models.CharField(primary_key=True, max_length=10, default=generate_nanoid, editable=False)
    firstName = models.CharField(max_length=50, null=False)
    lastName = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to="static/actors/image", null=True, blank=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"



class EventActors(models.Model):
    id = models.CharField(primary_key=True, max_length=10, default=generate_nanoid, editable=False)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actors, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, null=True, blank=True)


class Seat(models.Model):
    id = models.CharField(primary_key=True, max_length=10, default=generate_nanoid, editable=False)
    row = models.IntegerField()
    number = models.IntegerField()
    status = models.CharField(max_length=10, choices=[('available', 'Available'), ('booked', 'Booked')],default='available')
    event_time = models.ForeignKey(EventTime, on_delete=models.CASCADE, related_name="seats", null=True, blank=True)

    def __str__(self):
        return (f"Row {self.row}, Seat {self.number} "
                f"on {self.event_time.event.name} {self.event_time.date.strftime('%Y-%m-%d %H:%M')}")

    class Meta:
        ordering = ['row', 'number']


class Tickets(models.Model):
    id = models.CharField(primary_key=True, max_length=10, default=generate_nanoid, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, null=True, blank=True)  # Ссылка на Seat вместо прямого указания номеров
    purchase_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return (f"Ticket {self.id} for {self.seat.event_time.event.name} "
                f"on {self.seat.event_time.date.strftime('%Y-%m-%d %H:%M')}")
