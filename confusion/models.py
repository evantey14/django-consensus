from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.text import slugify
import random
import string


class RoomManager(models.Manager):
    def create_room(self, name):
        student_slug = slugify(name)
        teacher_slug = "".join(random.choice(string.ascii_uppercase) for i in range(6))
        room = self.create(name=name, student_slug=student_slug, teacher_slug=teacher_slug)
        return room

    def get_or_none(self, student_slug=None, teacher_slug=None):
        if student_slug is not None:
            return self.filter(student_slug=student_slug).first()
        if teacher_slug is not None:
            return self.filter(teacher_slug=teacher_slug).first()


class Room(models.Model):
    name = models.TextField()
    student_slug = models.SlugField(unique=True)
    teacher_slug = models.SlugField(unique=True)
    confused_students = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_students = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    objects = RoomManager()

    def increment_confused(self):
        self.confused_students += 1
        self.save()

    def decrement_confused(self):
        self.confused_students -= 1
        self.save()

    def increment_total(self):
        self.total_students += 1
        self.save()

    def decrement_total(self):
        self.total_students -= 1
        self.save()

    def __str__(self):
        return self.name
