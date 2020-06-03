from django.shortcuts import render

def index(request):
    return render(request, 'confusion/index.html')

def student(request, room_name):
    return render(request, 'confusion/student.html', {
        'room_name': room_name
    })

def teacher(request, room_name):
    return render(request, 'confusion/teacher.html', {
        'room_name': room_name
    })
