# Generated by Django 3.0.7 on 2020-06-05 04:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Confusion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confusion', to='confusion.Room')),
            ],
        ),
    ]
