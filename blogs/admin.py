from django.contrib import admin
from abstract_base_user_sample import User
from .models import Blog
from .models import Topic
from .models import Comment
from .models import Tag


admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Tag)

AUTH_USER_MODEL = 'abstract_base_user_sample.User'
