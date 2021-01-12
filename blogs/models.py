from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import date




class User(AbstractBaseUser):
    """Расширенная модель пользователей."""
    name = models.CharField(max_lenght=200, unique=True, blank=False,
            verbose_name="Имя(логин) пользователя")
    email = models.EmailField(unique=True, blank=False,
            verbose_name="Электронная почта")
    """..."""


class Blog(models.Model):
    """Модель блогов."""
    title = models.CharField(
        max_lenght=200, unique=True, verbose_name="Название блога"
    )
    description = models.TextField(null=True, verbose_name="Описание блога")
    date_add = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    date_edit = models.DateField(auto_now=True, verbose_name="Дата изменения")
    url = models.SlugField(max_lenght=200, unique=True)
    avatar = models.ImageField(
        upload_to='uploads/images/%Y/%m/%d/', max_lenght=250, null=True,
        verbose_name="Аватарка"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"


class Topic(models.Model):
    """Модель топиков"""
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, verbose_name="Блог"
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Имя автора"
    )
    title = models.CharField(
        max_lenght=200, unique=True, verbose_name="Название поста"
    )
    tags = models.CharField(
        max_lenght=250,
        default='',
        verbose_name="Список тегов(разделять запятой)"
    )
    hashtag = models.CharField(max_lenght=50, default='')
    date_add = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    date_edit = models.DateField(auto_now=True, verbose_name="Дата изменения")
    author_ip = models.GenericIPAddressField()
    flag_published = models.BooleanField(default=1)
    rating = models.DecimalField(max_digits=9, decimal_places=3, default=0)
    views = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )
    readings = models.PositiveIntegerField(
        default=0, verbose_name="Количество дочитываний"
    )
    votes_plus = models.PositiveIntegerField(
        default=0, verbose_name="Количество положительных голосов"
    )
    votes_minus = models.PositiveIntegerField(
        default=0, verbose_name="Количество отрицательных голосов"
    )
    comments_total = models.PositiveIntegerField(
        default=0, verbose_name="Количество комментариев"
    )
    last_comment = models.ForeignKey(
        'Comment', on_delete=models.CASCADE,
        verbose_name="Последний комментарий"
    )
    text = models.TextField(verbose_name="Содержимое топика")
    text_short = models.TextField(verbose_name="Краткое содержимое для превью")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Топик"
        verbose_name_plural = "Топики"
