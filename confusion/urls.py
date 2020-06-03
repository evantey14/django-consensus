from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('student/<str:room_name>/', views.student, name='student'),
    path('teacher/<str:room_name>/', views.teacher, name='teacher'),
]
