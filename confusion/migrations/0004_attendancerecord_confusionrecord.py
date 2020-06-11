# Generated by Django 3.0.7 on 2020-06-10 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('confusion', '0003_auto_20200610_0037'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfusionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action', models.IntegerField(choices=[(1, 'Confused'), (-1, 'Not Confused')])),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confusion.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action', models.IntegerField(choices=[(1, 'Joined'), (-1, 'Left')])),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confusion.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
