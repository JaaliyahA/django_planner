# Generated by Django 4.2.8 on 2023-12-11 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist',
            name='Date',
        ),
        migrations.AddField(
            model_name='daily',
            name='todolist',
            field=models.ManyToManyField(related_name='daily', to='planner.todolist'),
        ),
    ]
