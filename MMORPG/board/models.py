from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


# Create your models here.

class Ad(models.Model):
    CATEGORIES = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    title = models.CharField(max_length=200, db_index=True)
    description = HTMLField()
    category = models.CharField(max_length=100, choices=CATEGORIES, default='Танки')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('board:ad_detail', args=[str(self.id)])


class Response(models.Model):
    responseUser = models.ForeignKey(User, on_delete=models.CASCADE)
    responseText = models.TextField()
    responseAd = models.ForeignKey(Ad, on_delete=models.CASCADE)
    responseCreated_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Отклик на объявление '{self.responseAd.title}' от {self.responseUser.username}"
