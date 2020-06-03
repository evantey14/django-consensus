from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/student/(?P<room_name>\w+)/$", consumers.StudentConsumer),
    re_path(r"ws/teacher/(?P<room_name>\w+)/$", consumers.TeacherConsumer),
]
