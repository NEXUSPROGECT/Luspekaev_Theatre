from django.shortcuts import render
from .models import Events
from django.contrib.auth.models import User


# Create your views here.
def poster(request):
    return render(request, 'home.html')

def event(request, id):
    event_name = Events.objects.get(id=id).name

    context = {"event_id": id,
               "event_name": event_name}
    return render(request, 'event.html', context)

def ticket(request, id):
    context = {"ticket_id": id,
               "user_id": request.user.id}
    return render(request, 'tickets.html', context)

def mes(request):
    return render(request, 'mesTest.html')