from confusion.consumers.base import BaseConsumer
from confusion.constants import CLOSE_ROOM
from confusion.models import Room

class TeacherConsumer(BaseConsumer):
    def connect(self):
        self.teacher_group = self.scope['url_route']['kwargs']['teacher_slug']

        room = Room.objects.get(teacher_slug=self.teacher_group)
        self.student_group = room.student_slug

        self.group_add(self.teacher_group, self.channel_name)
        self.accept()

        self.update_confused_students()
        self.update_total_students()

    def receive_json(self, content):
        print(content)
        message = content['message']
        if (message == CLOSE_ROOM):
            self.group_send(self.teacher_group, {'type': 'close_room'})
            self.group_send(self.student_group, {'type': 'close_room'})
            Room.objects.get(teacher_slug=self.teacher_group).delete()

    def disconnect(self, close_code):
        self.group_discard(self.teacher_group, self.channel_name)

    def update_confused_students(self, event=None):
        room = Room.objects.get_or_none(teacher_slug=self.teacher_group)
        if room is not None:
            self.send_json({'confused_students': room.confused_students})

    def update_total_students(self, event=None):
        room = Room.objects.get_or_none(teacher_slug=self.teacher_group)
        if room is not None:
            self.send_json({'total_students': room.total_students})

    def close_room(self, event=None):
        self.send_json({'message': CLOSE_ROOM})
