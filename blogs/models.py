from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from datetime import date


class UserAccountManager(BaseUserManager):
    """Менеджер пользователей для расширенной модели пользователей"""
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Необходимо указать имя пользователя')
        if not email:
            raise ValueError('Необходимо указать адрес электронной почты')
        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Расширенная модель пользователей."""
    MALE = "Male"
    FEMALE = "Female"
    TARGET_TYPE_CHOICES = [
        (MALE, "Мужской"),
        (FEMALE, "Женский")
    ]

    username = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
        verbose_name="Имя(логин) пользователя"
    )
    email = models.EmailField(
        unique=True, blank=False, verbose_name="Электронная почта"
    )
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    permissions = models.CharField(max_length=255, null=True)
    is_staff = models.BooleanField(default=0)
    is_active = models.BooleanField(default=1)
    is_superuser = models.BooleanField(default=0)
    last_login = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего посещения"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания профиля"
    )
    date_activated = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата активации профиля"
    )
    # ip_register = models.GenericIPAddressField(null=True)
    skill = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    rating = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    count_vote = models.PositiveIntegerField(default=0)
    activate_key = models.CharField(max_length=32, null=True, default="NULL")
    inviter = models.CharField(max_length=10, null=True, default="NULL")
    profile_sex = models.CharField(max_length=10, choices=TARGET_TYPE_CHOICES)
    profile_country = models.CharField(max_length=30, null=True, default="NULL")
    profile_region = models.CharField(max_length=30, null=True, default="NULL")
    profile_city = models.CharField(max_length=30, null=True, default="NULL")
    profile_birthday = models.DateField(blank=True, null=True, default=None)
    profile_about = models.TextField(null=True, default="NULL")
    profile_avatar = models.ImageField(
        upload_to='uploads/images/%Y/%m/%d/%H/%M/%S/', max_length=250, null=True
    )
    settings_notice_new_topic = models.BooleanField(default=1)
    settings_notice_new_comment = models.BooleanField(default=1)
    settings_notice_new_message = models.BooleanField(default=1)
    settings_notice_reply_comment = models.BooleanField(default=1)
    settings_notice_new_comment_to_topic = models.BooleanField(default=1)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = UserAccountManager()

    def get_short_name(self):
        return self.username

    def __str__(self):
        return username

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

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Blog(models.Model):
    """Модель блогов."""
    title = models.CharField(
        max_length=200, unique=True, verbose_name="Название блога"
    )
    description = models.TextField(null=True, verbose_name="Описание блога")
    date_add = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    date_edit = models.DateTimeField(
        auto_now=True, verbose_name="Дата изменения"
    )
    url = models.SlugField(max_length=200, unique=True)
    avatar = models.ImageField(
        upload_to='uploads/images/%Y/%m/%d/%H/%M/%S/',
        max_length=250,
        null=True,
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
    title = models.CharField(max_length=200, verbose_name="Название поста")
    tags = models.CharField(
        max_length=250,
        default='',
        verbose_name="Список тегов(разделять запятой)"
    )
    hashtag = models.CharField(max_length=50, default='')
    date_add = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    date_edit = models.DateTimeField(
        auto_now=True, null=True, verbose_name="Дата изменения"
    )
    author_ip = models.GenericIPAddressField()
    is_published = models.BooleanField(default=1)
    is_delete = models.BooleanField(default=0)
    rating = models.DecimalField(max_digits=9, decimal_places=2, default=0)
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
    text = models.TextField(verbose_name="Содержимое топика")
    text_short = models.TextField(verbose_name="Краткое содержимое для превью")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Топик"
        verbose_name_plural = "Топики"


class Comment(models.Model):
    """Модель комментариев."""
    TOPIC = 'topic'
    TALK = 'talk'
    TARGET_TYPE_CHOICES = [
        (TOPIC, "Комментарий к топику"),
        (TALK, "Личное сообщение")
    ]

    pid = models.PositiveIntegerField(null=True)
    target_id = models.PositiveIntegerField()
    target_type = models.CharField(
        max_length=10, choices=TARGET_TYPE_CHOICES
    )
    target_blog_id = models.PositiveIntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_add = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    date_edit = models.DateTimeField(
        auto_now=True, null=True, verbose_name="Дата изменения"
    )
    last_editor_id = models.PositiveIntegerField(null=True)
    author_ip = models.GenericIPAddressField()
    rating = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    votes_plus = models.PositiveIntegerField(
        default=0, verbose_name="Количество положительных голосов"
    )
    votes_minus = models.PositiveIntegerField(
        default=0, verbose_name="Количество отрицательных голосов"
    )
    is_published = models.BooleanField(default=1)
    is_delete = models.BooleanField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Tag(models.Model):
    """Модель тегов"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.CharField(max_length=150, default='')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
