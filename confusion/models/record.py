from django.db import models

class RecordManager(models.Manager):
    def plus_one(self, room):
        return self.create(room=room, action=1)

    def minus_one(self, room):
        return self.create(room=room, action=-1)

    def get_history(self, room):
        records = self.filter(room=room).order_by('timestamp')
        times, counts = [], []
        count = 0
        history = {'times': [], 'attendance': []}
        for record in records:
            times.append(record.timestamp.__str__())
            count += record.action
            counts.append(count)
        return times, counts 

class Actions(models.IntegerChoices):
    PLUS_ONE = 1
    MINUS_ONE = -1

class SignedRecord(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    action = models.IntegerField(choices=Actions.choices)
    objects = RecordManager()

    class Meta:
        abstract = True

class AttendanceRecord(SignedRecord):
    pass

class ConfusionRecord(SignedRecord):
    pass
