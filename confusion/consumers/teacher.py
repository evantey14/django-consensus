import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from confusion.models import Room

class TeacherConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        room, _ = Room.objects.get_or_create(name=self.room_name)

        self.teacher_group = 'teacher.%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(self.teacher_group, self.channel_name)

        self.accept()
        self.update_confused_students()
        self.update_total_students()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.teacher_group, self.channel_name)

    def update_confused_students(self, event=None):
        room = Room.objects.get(name=self.room_name)
        self.send(text_data=json.dumps({
            'confused_students': room.confused_students
        }))

    def update_total_students(self, event=None):
        room = Room.objects.get(name=self.room_name)
        self.send(text_data=json.dumps({
            'total_students': room.total_students
        }))

