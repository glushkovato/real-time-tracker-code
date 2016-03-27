from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Board(models.Model):
    author = models.ForeignKey(User)  # ссылка на другую модель
    title = models.CharField(max_length=100)  # так мы определяем текстовое поле с ограничением на количество символов
    text = models.TextField(null=True)  # так определяется поле для неограниченно длинного текста
    created_date = models.DateTimeField(  # дата и время
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    # last_modified = models.DateField(auto_now=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    # def save(self):
    #     self.modified_date = timezone.now()
    #     super(Board, self).save()


class Card(models.Model):

    board = models.ForeignKey(Board)
    title = models.CharField(max_length=50)
    text = models.TextField(blank=True)
    created_date = models.DateTimeField(  # дата и время
            default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title


class Task(models.Model):
    card = models.ForeignKey(Card)
    title = models.CharField(max_length=200)
    deadline = models.DateField(blank=True, null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
