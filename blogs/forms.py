from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm as UCF

from .models import User


class UserCreationForm(UCF):
    error_css_class = 'error'
    required_css_class = 'required'
    # """A form for creating new users. Includes all the required
    # fields, plus a repeated password."""
    # password1 = forms.CharField(
    #     label='Пароль',
    #     widget=forms.PasswordInput,
    #     help_text=password_validation.password_validators_help_text_html(),
    # )
    # password2 = forms.CharField(
    #     label='Подтверждение пароля',
    #     widget=forms.PasswordInput,
    # )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError('Пароли не совпадают')
    #     return password2
    #
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password1'])
    #     if commit:
    #         user.save()
    #     return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_staff',)

    def clean_password(self):
        password = ReadOnlyPasswordHashField()
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial[password]
