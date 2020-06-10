from confusion.consumers.base import BaseConsumer
from confusion.constants import CLOSE_ROOM, CONFUSED, NOT_CONFUSED
from confusion.models import Room

class StudentConsumer(BaseConsumer):
    def connect(self):
        self.student_group = self.scope['url_route']['kwargs']['student_slug']
        self.is_confused = False

        room = Room.objects.get(student_slug=self.student_group)
        self.teacher_group = room.teacher_slug
        room.increment_total()
        self.group_send(self.teacher_group, {'type': 'update_total_students'})

        self.group_add(self.student_group, self.channel_name)
        self.accept()

    def receive_json(self, content):
        print(content)
        message = content['message']
        room = Room.objects.get(student_slug=self.student_group)
        if message == CONFUSED:
            room.increment_confused()
            self.is_confused = True
        elif message == NOT_CONFUSED:
            room.decrement_confused()
            self.is_confused = False

        self.group_send(self.teacher_group, {'type': 'update_confused_students'})

    def disconnect(self, close_code):
        room = Room.objects.get_or_none(student_slug=self.student_group)
        if room is not None:
            if self.is_confused:
                room.decrement_confused()
                self.group_send(self.teacher_group, {'type': 'update_confused_students'})
            room.decrement_total()
            self.group_send(self.teacher_group, {'type': 'update_total_students'})

        self.group_discard(self.student_group, self.channel_name)

    def close_room(self, event=None):
        self.send_json({'message': CLOSE_ROOM})
