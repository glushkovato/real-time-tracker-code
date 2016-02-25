from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User')  # ссылка на другую модель
    title = models.CharField(max_length=200)  # так мы определяем текстовое поле с ограничением на количество символов
    text = models.TextField()  # так определяется поле для неограниченно длинного текста
    created_date = models.DateTimeField(  # дата и время
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# Create your models here.
#class Task(models):
#    pass
