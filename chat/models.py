from django.db import models

from users.models import User


class Message(models.Model):
    """
    Модель для хранения сообщений чата.

    Класс Message представляет собой модель, используемую для хранения сообщений чата.
    Сообщение содержит информацию об отправителе, получателе, тексте сообщения,
    временной метке отправки, статусе прочтения и связи с каналом общения.
    """
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reciever = models.ForeignKey(User, related_name='to_reciever', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    channel = models.ForeignKey('ChannelNames', on_delete=models.CASCADE, related_name='channel_messages',
                                null=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    @staticmethod
    def create_object(new_sender_pk, new_receiver_pk, new_content, channel_pk):
        """
        Создание объекта сообщения.
        Метод create_object создает новый объект сообщения на основе предоставленных данных
        и сохраняет его в базе данных.
        """

        Message.objects.create(sender=User.objects.get(pk=new_sender_pk),
                               reciever=User.objects.get(pk=new_receiver_pk),
                               content=new_content,
                               channel=ChannelNames.objects.get(pk=channel_pk))


class ChannelNames(models.Model):
    """
        Модель для хранения Названий каналов общения.
        Класс ChannelNames представляет собой модель, используемую для хранения
        идентификаторов каналов общения между пользователями.
    """
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_user')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_user')
    channel_name = models.TextField()
