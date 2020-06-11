from django.contrib import admin

from confusion.models import AttendanceRecord, ConfusionRecord, Room

admin.site.register(AttendanceRecord)
admin.site.register(ConfusionRecord)
admin.site.register(Room)
