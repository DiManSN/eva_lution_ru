from django.contrib.auth.backends import ModelBackend

from .models import User


class AuthBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']
        try:
            user = User.objects.get(username=username)
            if user.user.check_password(password) is True:
                return customer.user
        except User.DoesNotExist:
            pass


# def authenticate(self, request=None, username=None, email=None, password=None):
#     if None in [email, password]:
#       return None
#     scope = locals()
#     data = {i: eval(i, scope) for i in ['username', 'email', 'password'] if eval(i, scope) is not None}
#     try:
#       password = data.pop('password')
#       user = User.objects.get(**data)
#       if not user.check_password(password):
#         return None
#     except:
#       return None
#     return user
#   def get_user(self, iden):
#     return User.objects.get(id=iden)
