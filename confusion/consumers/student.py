from confusion.consumers.base import BaseConsumer
from confusion.constants import CLOSE_ROOM, CONFUSED, NOT_CONFUSED
from confusion.models import AttendanceRecord, Room

class StudentConsumer(BaseConsumer):
    def connect(self):
        self.student_group = self.scope['url_route']['kwargs']['student_slug']
        self.is_confused = False

        room = Room.objects.get(student_slug=self.student_group)
        self.teacher_group = room.teacher_slug

        attendance_record = room.add_student()
        self.send_update_to_teachers('update_total_students', attendance_record)

        self.group_add(self.student_group, self.channel_name)
        self.accept()

    def receive_json(self, content):
        message = content['message']
        room = Room.objects.get(student_slug=self.student_group)
        if message == CONFUSED:
            confusion_record = room.add_confusion()
            self.is_confused = True
        elif message == NOT_CONFUSED:
            confusion_record = room.remove_confusion()
            self.is_confused = False
        self.send_update_to_teachers('update_confused_students', confusion_record)

    def disconnect(self, close_code):
        room = Room.objects.get_or_none(student_slug=self.student_group)
        if room is not None:
            if self.is_confused:
                confusion_record = room.remove_confusion()
                self.send_update_to_teachers('update_confused_students', confusion_record)
            attendance_record = room.remove_student()
            self.send_update_to_teachers('update_total_students', attendance_record)
        self.group_discard(self.student_group, self.channel_name)

    def send_update_to_teachers(self, update_type, record):
        self.group_send(self.teacher_group, {
            'type': update_type,
            'timestamp': record.timestamp.__str__(),
            'action': record.action,
        })

    def close_room(self, event=None):
        self.send_json({'message': CLOSE_ROOM})
