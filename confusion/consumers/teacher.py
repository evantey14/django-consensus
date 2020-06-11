from confusion.consumers.base import BaseConsumer
from confusion.constants import CLOSE_ROOM
from confusion.models import AttendanceRecord, Room

class TeacherConsumer(BaseConsumer):
    def connect(self):
        self.teacher_group = self.scope['url_route']['kwargs']['teacher_slug']

        room = Room.objects.get(teacher_slug=self.teacher_group)
        self.student_group = room.student_slug

        self.group_add(self.teacher_group, self.channel_name)
        self.accept()

        self.initialize_plots()

    def receive_json(self, content):
        message = content['message']
        if (message == CLOSE_ROOM):
            self.group_send(self.teacher_group, {'type': 'close_room'})
            self.group_send(self.student_group, {'type': 'close_room'})
            Room.objects.get(teacher_slug=self.teacher_group).delete()

    def disconnect(self, close_code):
        self.group_discard(self.teacher_group, self.channel_name)

    def initialize_plots(self):
        room = Room.objects.get(teacher_slug=self.teacher_group)
        self.send_json({'type': 'initialize_plots', 'history': room.get_history()})

    def update_confused_students(self, event):
        self.send_json({
            'type': 'update_confused_students',
            'timestamp': event.get('timestamp'),
            'action': event.get('action'),
        })

    def update_total_students(self, event):
        self.send_json({
            'type': 'update_total_students',
            'timestamp': event.get('timestamp'),
            'action': event.get('action')
        })

    def close_room(self, event=None):
        self.send_json({'type': CLOSE_ROOM})
