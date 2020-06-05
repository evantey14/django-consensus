import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

from confusion.constants import CONFUSED, NOT_CONFUSED
from confusion.models import Room

class StudentConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.student_group = 'student.%s' % self.room_name
        self.teacher_group = 'teacher.%s' % self.room_name

        self.room, _ = Room.objects.get_or_create(name=self.room_name)
        self.room.total_students += 1
        self.room.save()

        async_to_sync(self.channel_layer.group_add)(self.student_group, self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            self.teacher_group, {'type': 'update_total_students'}
        )
        self.accept()

    def disconnect(self, close_code):
        room = Room.objects.get(name=self.room_name)
        self.room.total_students -= 1
        self.room.save()

        async_to_sync(self.channel_layer.group_send)(
            self.teacher_group, {'type': 'update_total_students'}
        )
        async_to_sync(self.channel_layer.group_discard)(self.student_group, self.channel_name)

    def receive(self, text_data):
        print(text_data)
        message = json.loads(text_data)['message']
        room = Room.objects.get(name=self.room_name)
        if message == CONFUSED:
            room.confused_students += 1
        elif message == NOT_CONFUSED:
            room.confused_students -= 1
        room.save()

        async_to_sync(self.channel_layer.group_send)(
            self.teacher_group, {'type': 'update_confused_students'}
        )
