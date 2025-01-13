import logging

logger = logging.getLogger(__name__)

from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Tickets, Seat

@receiver(post_delete, sender=Tickets)
def update_seat_status(sender, instance, **kwargs):
    # Пример: Обновление статуса места после удаления билета
    print("update_seat_status")
    if instance.seat:
        instance.seat.status = 'available'
        instance.seat.save()