# Generated by Django 4.2.1 on 2024-02-22 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='friends',
        ),
    ]
