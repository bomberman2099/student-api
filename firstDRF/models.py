from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', blank=True, null=True)
    title = models.CharField(max_length=50)
    text = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}: {self.text[:30]}'


class BlockUser(models.Model):
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f'{self.article} - {self.text[:30]}'
