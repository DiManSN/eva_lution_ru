from django.shortcuts import render
from django.views.generic.base import View

from .models import Blog


class BlogView(View):
    """Список блогов"""
    def get(self, request):
        blogs = Blog.objects.all()
        return render(request, 'blogs/blog_list.html', {'blog_list': blogs})
