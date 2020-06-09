import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from confusion.constants import CLOSE_ROOM
from confusion.models import Room

class TeacherConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        room, _ = Room.objects.get_or_create(name=self.room_name)

        self.teacher_group = 'teacher.%s' % self.room_name
        self.student_group = 'student.%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(self.teacher_group, self.channel_name)

        self.accept()
        self.update_confused_students()
        self.update_total_students()

    def receive(self, text_data):
        print(text_data)
        message = json.loads(text_data)['message']
        if (message == CLOSE_ROOM):
            async_to_sync(self.channel_layer.group_send)(self.teacher_group, {'type': 'close_room'})
            async_to_sync(self.channel_layer.group_send)(self.student_group, {'type': 'close_room'})
            Room.objects.get(name=self.room_name).delete()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.teacher_group, self.channel_name)

    def update_confused_students(self, event=None):
        room = Room.objects.get_or_none(name=self.room_name)
        if room is not None:
            self.send(text_data=json.dumps({'confused_students': room.confused_students}))

    def update_total_students(self, event=None):
        room = Room.objects.get_or_none(name=self.room_name)
        if room is not None:
            self.send(text_data=json.dumps({'total_students': room.total_students}))

    def close_room(self, event=None):
        self.send(text_data=json.dumps({'message': CLOSE_ROOM}))
