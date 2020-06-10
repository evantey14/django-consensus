from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-room', views.create_room, name='create-room'),
    path('student/<slug:student_slug>/', views.student, name='student'),
    path('teacher/<slug:teacher_slug>/', views.teacher, name='teacher'),
]
