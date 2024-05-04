# Generated by Django 4.2.1 on 2024-03-22 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_channelnames_channel_messages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channelnames',
            name='channel_messages',
        ),
        migrations.AddField(
            model_name='message',
            name='channel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='channel_messages', to='chat.message'),
        ),
    ]
