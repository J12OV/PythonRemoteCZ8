from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from chatterbox.models import Room, Message



# Create your views here.
def hello(request, s):
    return HttpResponse(f'Hello, {s} world!')

def home(request):
    rooms = Room.objects.all()  # najdeme všechny místnosti,

    context = {'rooms': rooms}
    return render(request, 'chatterbox/home.html', context)

@login_required
def search(request, s):
    rooms = Room.objects.filter(name__contains=s)
    messages = Message.objects.filter(body__contains=s)

    context = {'rooms': rooms, 'messages': messages}
    return render(request, "chatterbox/search.html", context)

    # response = "Rooms: "
    # for room in rooms:
    #    response += room.name + ", "


    # response += "<br>Messages: "
    #for message in messages:
    #    response += message.body[0:10] + " ... , "

@login_required
def room(request, pk):
    room = Room.objects.get(id=pk)  # najdeme místnost se zadaným id
    messages = Message.objects.filter(room=pk)
    context = {'room': room, 'messages': messages}
    return render(request, "chatterbox/room.html", context) #TODO: vytvořit template

@login_required
def rooms(request):
    rooms = Room.objects.all()

    context = {'rooms':rooms}
    return render(request, "chatterbox/rooms.html", context)