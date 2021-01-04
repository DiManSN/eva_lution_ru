from django.db import models
from django.contrib.auth import get_user_model
from datetime import date


User = get_user_model()


class Blog(models.Model):
    """Модель блогов."""
    title = models.CharField(max_lenght=200, unique=True,
            verbose_name="Название блога")
    description = models.TextField(null=True, verbose_name="Описание блога")
    date_add = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    date_edit = models.DateField(auto_now=True, verbose_name="Дата изменения")
    url = models.SlugField(max_lenght=200, unique=True)
    avatar = models.ImageField(upload_to='uploads/images/%Y/%m/%d/',
            max_lenght=250, null=True, verbose_name="Аватарка")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "blogs"
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"


class Topic(object):
    """Модель топиков"""
    blog = models.ForeignKey(Blog, verbose_name="Блог",
            on_delete=models.CASCADE)
    author = models.ForeignKey(User, )
    title = models.CharField(max_lenght=200, unique=True,
            verbose_name="Название поста")
