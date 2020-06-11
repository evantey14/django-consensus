from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.text import slugify
import random
import string

from .record import AttendanceRecord, ConfusionRecord

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
    objects = RoomManager()

    @property
    def confused_students(self):
        return ConfusionRecord.objects.filter(room=self).aggregate(models.Sum('action'))

    @property
    def total_students(self):
        return AttendanceRecord.objects.filter(room=self).aggregate(models.Sum('action'))

    def add_student(self):
        return AttendanceRecord.objects.plus_one(self) 

    def remove_student(self):
        return AttendanceRecord.objects.minus_one(self) 

    def add_confusion(self):
        return ConfusionRecord.objects.plus_one(self)

    def remove_confusion(self):
        return ConfusionRecord.objects.minus_one(self)

    def get_history(self):
        attendance_times, attendance_records = AttendanceRecord.objects.get_history(self)
        confusion_times, confusion_records = ConfusionRecord.objects.get_history(self)
        history = {
            'attendance_times': attendance_times, 'attendance': attendance_records,
            'confusion_times': confusion_times, 'confusion': confusion_records,
        }
        return history

    def __str__(self):
        return self.name
