from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import date




class User(AbstractBaseUser):
    """Расширенная модель пользователей."""
    MALE = "Male"
    FEMALE = "Female"
    TARGET_TYPE_CHOICES = [
        (MALE, "Мужской")
        (FEMALE, "Женский")
    ]

    name = models.CharField(
        max_lenght=200,
        unique=True,
        blank=False,
        verbose_name="Имя(логин) пользователя"
    )
    email = models.EmailField(
        unique=True, blank=False, verbose_name="Электронная почта"
    )
    first_name = models.CharField(max_lenght=50, null=True)
    last_name = models.CharField(max_lenght=50, null=True)
    permissions = models.CharField(max_lenght=255)
    is_staff = models.BooleanField(default=0)
    is_active = models.BooleanField(default=0)
    is_superuser = models.BooleanField(default=0)
    last_login = models.DateField(
        auto_now=True, verbose_name="Дата последнего посещения"
    )
    date_joined = models.DateField(
        auto_now_add=True, verbose_name="Дата создания профиля"
    )
    date_activated = models.DateField(
        auto_now_add=True, verbose_name="Дата активации профиля"
    )
    ip_register = models.GenericIPAddressField()
    skill = models.DecimalField(max_digits=9, decimal_places=3, default=0)
    rating = models.DecimalField(max_digits=9, decimal_places=3, default=0)
    count_vote = models.PositiveIntegerField(default=0)
    activate_key = models.CharField(max_lenght=32, null=True, default='NULL')
    inviter = models.ForeignKey(
        self,
        on_delete=models.CASCADE,
        null=True,
        default='NULL'
    )
    profile_sex = models.CharField(max_lenght=10, choices=TARGET_TYPE_CHOICES)
    profile_country = models.CharField(max_lenght=30, null=True, default="NULL")
    profile_region = models.CharField(max_lenght=30, null=True, default="NULL")
    profile_city = models.CharField(max_lenght=30, null=True, default="NULL")
    profile_birthday = models.DateField(null=True, default="NULL")
    profile_about = models.TextField(null=True, default="NULL")
    profile_avatar = models.ImageField(
        upload_to='uploads/images/%Y/%m/%d/', max_lenght=250, null=True
    )
    settings_notice_new_topic = models.BooleanField(default=1)
    settings_notice_new_comment = models.BooleanField(default=1)
    settings_notice_new_message = models.BooleanField(default=1)
    settings_notice_reply_comment = models.BooleanField(default=1)
    settings_notice_new_comment_to_topic = models.BooleanField(default=1)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'name'

    def __str__(self):
        return name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


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
    is_published = models.BooleanField(default=1)
    is_delete = models.BooleanField(default=0)
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
    TARGET_TYPE_CHOICES[
        (TOPIC, "Комментарий к топику"),
        (TALK, "Личное сообщение")
    ]

    pid = models.PositiveIntegerField(null=True)
    target_id = models.PositiveIntegerField()
    target_type = models.CharField(
        max_lenght=10, choices=TARGET_TYPE_CHOICES
    )
    target_blog_id = models.PositiveIntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_add = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    date_edit = models.DateField(auto_now=True, verbose_name="Дата изменения")
    last_editor_id = models.PositiveIntegerField()
    author_ip = models.GenericIPAddressField()
    rating = models.DecimalField(max_digits=9, decimal_places=3, default=0)
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
        topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
        user_id = models.ForeignKey(User, on_delete=models.CASCADE)
        blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
        text = models.CharField(max_lenght=150, default='')

        def __str__(self):
            return self.text

        class Meta:
            verbose_name = "Тег"
            verbose_name_plural = "Теги"
