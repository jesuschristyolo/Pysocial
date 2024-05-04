# Generated by Django 4.2.1 on 2024-03-13 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_alter_channelnames_first_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channelnames',
            name='first_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_user', to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='channelnames',
            name='second_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_user', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
