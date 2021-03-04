from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .forms import UserCreationForm, UserChangeForm
from .models import Blog, Comment, Tag, Topic, User


admin.site.register(Blog)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    date_hierarchy = 'date_activated'

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('username', 'email', 'is_staff', 'last_login',)
    list_filter = ('is_staff', 'is_active',)
    # if form:
    #     readonly_fields = ('username', 'email', 'first_name', 'last_name',)
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Персональная инфомация', {'fields': ('email', 'first_name', 'last_name',)}),
        ('Права доступа', {'fields': ('is_staff', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('user',),
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'password1', 'password2'
            ),
        }),
    )
    search_fields = ('username', 'email',)
    ordering = ('username',)
    filter_horizontal = ()


class TopicAdmin(admin.ModelAdmin):
    model = Topic
    date_hierarchy = 'date_add'
    list_display = ('title', 'blog', 'author')
    list_filter = ('date_add',)

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Topic, TopicAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


AUTH_USER_MODEL = 'blogs.User'
