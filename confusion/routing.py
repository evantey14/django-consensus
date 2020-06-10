from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/student/(?P<student_slug>[\w-]+)/", consumers.StudentConsumer),
    re_path(r"ws/teacher/(?P<teacher_slug>[\w-]+)/", consumers.TeacherConsumer),
]
