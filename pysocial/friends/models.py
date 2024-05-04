from django.conf import settings
from django.db import models


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender", null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver", null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)






