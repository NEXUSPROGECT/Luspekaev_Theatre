from multiprocessing.reduction import register

from django.contrib import admin
from .utils import populate_seats
from .models import Events, EventTime, EventImportant, EventImage, Actors, EventActors, Tickets, Seat

# Register your models here.
admin.site.register(Events)

admin.site.register(EventImportant)
admin.site.register(EventImage)
admin.site.register(Actors)
admin.site.register(EventActors)
admin.site.register(Seat)
admin.site.register(Tickets)

@admin.action(description='Создать места для события')
def generate_seats(modeladmin, request, queryset):
    for event_time in queryset:
        seats_matrix = [21, 23, 25, 27, 29, 31, 33, 34, 34, 34, 34, 34, 28, 34, 34, 34, 34, 34, 34, 34, 34, 34, 16, 10]  # Например, фиксированная матрица
        populate_seats(event_time.id, seats_matrix)

@admin.register(EventTime)
class EventTimeAdmin(admin.ModelAdmin):
    actions = [generate_seats]

