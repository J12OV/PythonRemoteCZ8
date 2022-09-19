from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.
class Room(models.Model):
 #   host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-updated']  # descending order


    def __str__(self):
        return self.name

    def messages_count(self):
        room_messages = self.message_set.all()
        return room_messages.count()

    def last_message_time(self):
        room_message = self.message_set.all()[0]
        return room_message.updated

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created','-updated']   # descending order

    def __str__(self):
        return self.body[0:50]


"""
mistnost = Room()
mistnost.name ="Jmeno"
misnost.description = "

print(mistnost)

First import !!!

Python Django shell
(SELECT * FROM Room)
Room.objects.all()

Najdi ROOM obsahující “Django” v sloupečku name
(SELECT * FROM Room Where name LIKE "Django")
Room.objects.filetr(name__contains="Django")

Vrať ROOM s “Python” v názvu (Přesně!) (SELECT * FROM Room Where name="Python")
Room.objects.get(name="Python")

Složená podmínka ve WHERE lze použít logické operátory (“|” = OR/nebo, “&” = AND/a)
Room.objects.filter(
  Q(name__contains="Django") |
  Q(name__startswith="Python")
)
"""