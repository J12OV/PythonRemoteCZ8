from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from chatterbox.models import Room, Message


# Create your views here.
def hello(request, s):
    return HttpResponse(f'Hello, {s} world!')


def home(request):
    rooms = Room.objects.all()  # najdeme všechny místnosti

    context = {'rooms': rooms}
    return render(request, 'chatterbox/home.html', context)


@login_required
def search(request):
    if request.method == 'POST':  # pokud pošleme dotaz z formuláře
        s = request.POST.get('search')                       # z odeslané proměnné si vytáhnu, co chci hledat
        s = s.strip()                                        # ořízneme prázdné znaky
        if len(s) > 0:                                       # pkud s obsahuje alespoň jeden znak
            rooms = Room.objects.filter(name__contains=s)        # vyfiltruji místnosti dle zadaného řetězce
            messages = Message.objects.filter(body__contains=s)  # vyfiltruji zprávy dle zadaného řetezce

            context = {'rooms': rooms, 'messages': messages, 'search': s }     # výsledky uložím do kontextu
            return render(request, "chatterbox/search.html", context)  # vykreslíme stránku s výsledky
        return redirect('home')
                                                         # pokud POST nebyl odeslán
    # context = {'rooms': None, 'messages': None}        # místnosti i zprávy budou prázdné
    return redirect('home')                              # případně lze přesměrovat na jinou stránku

# @login_required
# def search(request, s):
#         rooms = Room.objects.filter(name__contains=s)
#         messages = Message.objects.filter(body__contains=s)
#
#         context = {'rooms': rooms, 'messages': messages}
#     return render(request, "chatterbox/search.html", context)

@login_required
def room(request, pk):
    room = Room.objects.get(id=pk)  # najdeme místnost se zadaným id
    messages = Message.objects.filter(room=pk)  # vybereme všechny zprávy dané místnosti

    # pokud zadáme novou zprávu, musíme ji zpracovat
    if request.method == 'POST':
        file_url = ""
        if request.FILES.get('upload'):                             # pokud jsme poslali soubor přidáním get -->bez obrázku
            upload = request.FILES['upload']                    # z requestu si vytáhnu soubor
            file_storage = FileSystemStorage()                  # práce se souborovým systémem
            file = file_storage.save(upload.name, upload)       # uložíme soubor na disk
            file_url = file_storage.url(file)                   # vytáhnu ze souboru url adresu a uložím
        body = request.POST.get('body').strip()
        if len(body) > 0 or request.FILES['upload']:
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=body,
                file=file_url                                   # vložíme url
            )
        return HttpResponseRedirect(request.path_info)

    context = {'room': room, 'messages': messages}
    return render(request, "chatterbox/room.html", context)

@login_required
def rooms(request):
    rooms = Room.objects.all()

    context = {'rooms': rooms}
    return render(request, "chatterbox/rooms.html", context)


@login_required
def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        descr = request.POST.get('descr').strip()
        if len(name) > 0 and len(descr) > 0:
            room = Room.objects.create(
                host=request.user,
                name=name,
                description=descr
            )

            return redirect('room', pk=room.id)

    return render(request, 'chatterbox/create_room.html')


@login_required
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if room.messages_count() == 0:  # pokud v místnosti není žádná zpráva
        room.delete()               # tak místnost smažeme

        return redirect('rooms')

    context = {'room': room, 'message_count': room.messages_count()}
    return render(request, 'chatterbox/delete_room.html', context)

def delete_room_yes(request, pk):
    room = Room.objects.get(id=pk)
    room.delete()               # tak místnost smažeme
    return redirect('rooms')






# formulář
class RoomEditForm(ModelForm):

    class Meta:
        model = Room
        fields = '__all__'

#view
@method_decorator(login_required, name ='dispatch')
class EditRoom(UpdateView):
    template_name='chatterbox/edit_room.html'
    model = Room
    form_class = RoomEditForm
    success_url = reverse_lazy('home')