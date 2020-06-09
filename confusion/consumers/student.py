from confusion.consumers.base import BaseConsumer
from confusion.constants import CLOSE_ROOM, CONFUSED, NOT_CONFUSED
from confusion.models import Room

class StudentConsumer(BaseConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.student_group = 'student.%s' % self.room_name
        self.teacher_group = 'teacher.%s' % self.room_name

        room, _ = Room.objects.get_or_create(name=self.room_name)
        room.increment_total()
        self.group_send(self.teacher_group, {'type': 'update_total_students'})

        self.group_add(self.student_group, self.channel_name)
        self.accept()

    def receive_json(self, content):
        print(content)
        message = content['message']
        room = Room.objects.get(name=self.room_name)
        if message == CONFUSED:
            room.increment_confused()
        elif message == NOT_CONFUSED:
            room.decrement_confused()

        self.group_send(self.teacher_group, {'type': 'update_confused_students'})

    def disconnect(self, close_code):
        room = Room.objects.get_or_none(name=self.room_name)
        if room is not None:
            room.decrement_total()
            self.group_send(self.teacher_group, {'type': 'update_total_students'})
            self.group_discard(self.student_group, self.channel_name)

    def close_room(self, event=None):
        self.send_json({'message': CLOSE_ROOM})
