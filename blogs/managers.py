from django.contrib.auth.models import BaseUserManager


class UserAccountManager(BaseUserManager):
    """Менеджер пользователей для расширенной модели пользователей"""
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Необходимо указать имя пользователя')
        if not email:
            raise ValueError('Необходимо указать адрес электронной почты')
        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
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

    def get_by_natural_key(self, username_):
        return self.get(username=username_)


# class MyUserManager(UserManager):
#   def create(self, **kwargs):
#     user = super().create(**kwargs)
#     user.set_password(user.password)
#     user.save()
#     return user
#   def get(self, **kwargs):
#     if kwargs.get('email', None) is not None:
#       return super().get(email=kwargs['email'])
#     elif kwargs.get('id', None) is not None:
#       return super().get(id=kwargs['id'])
#     return None
