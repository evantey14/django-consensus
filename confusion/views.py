from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import json

from confusion.models import Room

def index(request):
    return render(request, 'confusion/index.html')

def create_room(request):
    name = json.loads(request.body.decode('utf-8')).get('name')
    # TODO: validate name
    try:
        room = Room.objects.create_room(name)
        return JsonResponse({
            'name': room.name,
            'student_slug': room.student_slug,
            'teacher_slug': room.teacher_slug,
        })
    except IntegrityError:
        return JsonResponse({'error': 'Room already exists. Please pick a different name.'})

def student(request, student_slug):
    room = Room.objects.get_or_none(student_slug=student_slug)
    if room is None:
        return redirect(reverse('index'))
    else:
        return render(request, 'confusion/student.html', {'room_name': room.name})

def teacher(request, teacher_slug):
    room = Room.objects.get_or_none(teacher_slug=teacher_slug)
    if room is None:
        return redirect(reverse('index'))
    else:
        return render(request, 'confusion/teacher.html', {'room_name': room.name})
