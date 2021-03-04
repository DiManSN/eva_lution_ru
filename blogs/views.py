from django.shortcuts import render
from django.views.generic.base import View
from django.contrib import messages
from django.core.paginator import (EmptyPage, Paginator, PageNotAnInteger)
from django.shortcuts import redirect
from django.views.generic import ListView

from .forms import UserCreationForm
from .models import (Blog, Topic, TopicContent)


class BlogView(View):
    """Список блогов"""
    def get(self, request):
        blogs = Blog.objects.all()
        return render(request, 'blogs/blog_list.html', {'blog_list': blogs})


class TopicListView(ListView):
    """Список топиков на главную страницу с пагинацией."""
    def get(self, request):
        topic_list = Topic.objects.all().order_by('-date_add')
        paginator = Paginator(topic_list, 10)
        page_number = request.GET.get('page')        
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        return render(request, 'blogs/index.html', {'page_obj': page_obj})


def registration(request):

    if request.method == 'POST':
        # Создаём форму
        form = UserCreationForm(request.POST)
        # Валидация данных из формы
        if form.is_valid():
            # Сохраняем пользователя
            form.save()
            # Рендаринг страницы
            messages.success(request, 'Account created successfully')
            return redirect('/')
        else:
            return render(request, 'blogs/registration.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'blogs/registration.html', {'form': form})
