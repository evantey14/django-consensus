# Generated by Django 3.0.7 on 2020-06-10 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confusion', '0004_attendancerecord_confusionrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='total_students',
        ),
    ]
