# Generated by Django 4.2.1 on 2024-02-12 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='man',
            name='cat',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Man',
        ),
    ]