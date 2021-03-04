from datetime import date

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.db import models
from django.utils import timezone

from .managers import UserAccountManager


class User(AbstractBaseUser, PermissionsMixin):
    """Расширенная модель пользователей."""
    username = models.CharField('Имя(логин) пользователя', max_length=200, unique=True, blank=False)
    email = models.EmailField('Электронная почта', unique=True, blank=False)
    first_name = models.CharField('Имя', max_length=50, null=True, blank=True)
    last_name = models.CharField('Фамилия', max_length=50, null=True, blank=True)
    permissions = models.CharField(max_length=255, null=True)
    is_staff = models.BooleanField('Администратор', default=0)
    is_active = models.BooleanField('Активный', default=1)
    is_superuser = models.BooleanField(default=0)
    last_login = models.DateTimeField('Дата последнего посещения', auto_now=True)
    date_joined = models.DateTimeField('Дата создания профиля', auto_now_add=True)
    date_activated = models.DateTimeField('Дата активации профиля', auto_now_add=True)
    # ip_register = models.GenericIPAddressField(null=True)
    skill = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    rating = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    count_vote = models.PositiveIntegerField(default=0)
    activate_key = models.CharField(max_length=32, null=True, default='NULL')
    inviter = models.CharField(max_length=10, null=True, default='NULL')

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = UserAccountManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

class UserProfile(models.Model):
    """Модель данных профиля пользователя."""
    MALE = 'Male'
    FEMALE = 'Female'
    TARGET_TYPE_CHOICES = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский')
    ]

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, primary_key=True)
    sex = models.CharField(max_length=10, choices=TARGET_TYPE_CHOICES)
    country = models.CharField(max_length=30, null=True, default='NULL')
    region = models.CharField(max_length=30, null=True, default='NULL')
    city = models.CharField(max_length=30, null=True, default='NULL')
    birthday = models.DateField(blank=True, null=True, default=None)
    about = models.TextField(null=True, default='NULL')
    avatar = models.ImageField(upload_to='images/%Y/%m/%d/%H/%M/%S/', max_length=250, null=True)

    class Meta:
        db_table = 'blogs_user_profile'


class UserSettingsNotice(models.Model):
    """Модель настроек оповещений"""
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, primary_key=True)
    new_topic = models.BooleanField(default=1)
    new_comment = models.BooleanField(default=1)
    new_message = models.BooleanField(default=1)
    reply_comment = models.BooleanField(default=1)
    new_comment_to_topic = models.BooleanField(default=1)

    class Meta:
        db_table = 'blogs_user_settings_notice'


class Blog(models.Model):
    """Модель блогов."""
    title = models.CharField('Название блога', max_length=200, unique=True)
    description = models.TextField('Описание блога', null=True)
    date_add = models.DateTimeField('Дата создания', auto_now_add=True)
    date_edit = models.DateTimeField('Дата изменения', auto_now=True)
    url = models.SlugField(max_length=200, unique=True)
    avatar = models.ImageField('Аватарка', upload_to='images/%Y/%m/%d/%H/%M/%S/', max_length=250, null=True)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return self.title


class Topic(models.Model):
    """Модель топиков"""
    blog = models.ForeignKey(Blog, verbose_name='Блог', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Имя автора', on_delete=models.PROTECT)
    title = models.CharField('Название поста', max_length=200)
    tags = models.CharField('Список тегов(разделять запятой)', max_length=250, default='')
    hashtag = models.CharField(max_length=50, default='')
    date_add = models.DateTimeField('Дата создания', auto_now_add=True)
    date_edit = models.DateTimeField('Дата изменения', auto_now=True, null=True)
    author_ip = models.GenericIPAddressField()
    is_published = models.BooleanField(default=1)
    is_delete = models.BooleanField(default=0)
    rating = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    views = models.PositiveIntegerField('Количество просмотров', default=0)
    readings = models.PositiveIntegerField('Количество дочитываний', default=0)
    votes_plus = models.PositiveIntegerField('Количество положительных голосов', default=0)
    votes_minus = models.PositiveIntegerField('Количество отрицательных голосов', default=0)
    comments_total = models.PositiveIntegerField('Количество комментариев', default=0)

    class Meta:
        verbose_name = 'Топик'
        verbose_name_plural = 'Топики'

    def __str__(self):
        return self.title


class TopicContent(models.Model):
    """Содержимое топиков"""
    topic = models.OneToOneField(
        Topic, verbose_name='Топик', on_delete=models.CASCADE, primary_key=True, related_name='topic_texts'
    )
    text = models.TextField('Содержимое топика')
    text_short = models.TextField('Краткое содержимое для превью')

    class Meta:
        db_table = 'blogs_topic_content'

    def get_text_short(self, parent_id):
        return Topic.objects.filter(parent__id=self.topic).count()


class Comment(models.Model):
    """Модель комментариев."""
    TOPIC = 'topic'
    TALK = 'talk'
    TARGET_TYPE_CHOICES = [
        (TOPIC, 'Комментарий к топику'),
        (TALK, 'Личное сообщение')
    ]

    pid = models.PositiveIntegerField(null=True)
    target_id = models.PositiveIntegerField()
    target_type = models.CharField(max_length=10, choices=TARGET_TYPE_CHOICES)
    target_blog_id = models.PositiveIntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_add = models.DateTimeField('Дата создания', auto_now_add=True)
    date_edit = models.DateTimeField('Дата изменения', auto_now=True, null=True)
    last_editor_id = models.PositiveIntegerField(null=True)
    author_ip = models.GenericIPAddressField()
    rating = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    votes_plus = models.PositiveIntegerField('Количество положительных голосов', default=0)
    votes_minus = models.PositiveIntegerField('Количество отрицательных голосов', default=0)
    is_published = models.BooleanField(default=1)
    is_delete = models.BooleanField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Tag(models.Model):
    """Модель тегов"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.CharField(max_length=150, default='')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.text
