import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from confusion.constants import CONFUSED, NOT_CONFUSED

class TeacherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.confused_students = 0
        self.total_students = 0
        self.teacher_group = 'teacher.%s' % self.room_name
        print(self.channel_name, 'joining', self.teacher_group)
        await self.channel_layer.group_add(self.teacher_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.teacher_group, self.channel_name)

    async def confusion_message(self, event):
        message = event['message']
        if message == CONFUSED:
            self.confused_students += 1
        elif message == NOT_CONFUSED:
            self.confused_students -= 1
        print('teacher', self.channel_name, 'received', message)
        print('number of confused students', self.confused_students)
        await self.send(text_data=json.dumps({'confused_students':self.confused_students}))

    async def student_joined(self, event):
        self.total_students += 1
        await self.send(text_data=json.dumps({'total_students':self.total_students}))


    async def student_left(self, event):
        self.total_students -= 1
        await self.send(text_data=json.dumps({'total_students':self.total_students}))

