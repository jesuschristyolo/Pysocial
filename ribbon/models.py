from django.db import models

from users.models import User


class Posts(models.Model):
    """
    Модель для хранения постов.

    Модель Posts представляет собой записи в ленте социальной сети.
    Каждый пост содержит текстовое содержимое, автора поста,
    кодовое содержимое, выходное содержимое, а также информацию о времени создания.

    """

    author = models.ForeignKey(User, related_name='author_posts', on_delete=models.CASCADE)
    text_content = models.TextField(null=True)
    code_content = models.TextField(null=True)
    output_content = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def count_likes(self):
        return self.post_like.count()


class Comment(models.Model):
    """
    Модель для хранения комментариев к постам.
    Модель Comment представляет собой комментарии пользователей к постам в социальной сети. Каждый комментарий
    содержит текстовое содержимое, информацию об авторе, связь с соответствующим постом и временем создания.
    """

    author = models.ForeignKey(User, related_name='author_comment', on_delete=models.CASCADE)
    content = models.TextField(default="Null")
    post_comment = models.ForeignKey(Posts, related_name='post_comment', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class Like(models.Model):
    """
    Модель для хранения лайков к постам и комментариям.
    Модель Like представляет собой информацию о лайках, которые пользователи оставляют к постам и комментариям
    в социальной сети. Каждый лайк связан с определенным пользователем и либо с постом, либо с комментарием.

    """
    author = models.ForeignKey(User, related_name='author_like', on_delete=models.CASCADE)
    post_like = models.ForeignKey(Posts, related_name='post_like', on_delete=models.CASCADE, null=True)
    comment_like = models.ForeignKey(Comment, related_name='comment_like', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
