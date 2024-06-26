# Generated by Django 4.2.1 on 2024-02-14 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about_me',
            field=models.CharField(blank=True, null=True, verbose_name='Обо мне'),
        ),
        migrations.AddField(
            model_name='user',
            name='grade',
            field=models.IntegerField(choices=[(0, 'Начинающий'), (1, 'Джун'), (2, 'Джун +'), (3, 'Мидл'), (4, 'Синиор'), (5, 'Лид')], default=0, verbose_name='Разряд'),
        ),
        migrations.AddField(
            model_name='user',
            name='programming_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='время программирования'),
        ),
    ]
