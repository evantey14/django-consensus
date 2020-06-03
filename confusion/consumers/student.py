import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class StudentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.student_group = 'student.%s' % self.room_name
        self.teacher_group = 'teacher.%s' % self.room_name
        print(self.channel_name, 'joining', self.student_group)
        await self.channel_layer.group_add(self.student_group, self.channel_name)
        await self.channel_layer.group_send(self.teacher_group, {'type': 'student_joined'})
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(self.teacher_group, {'type': 'student_left'})
        await self.channel_layer.group_discard(self.student_group, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message, '->', self.teacher_group)
        await self.channel_layer.group_send(
            self.teacher_group,
            {
                'type': 'confusion_message',
                'message': message,
            }
        )
