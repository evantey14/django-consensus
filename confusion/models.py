from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class RoomManager(models.Manager):
    def get_or_none(self, name):
        return self.filter(name=name).first()

class Room(models.Model):
    name = models.TextField(unique=True)
    confused_students = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_students = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    objects = RoomManager()

    def __str__(self):
        return self.name
