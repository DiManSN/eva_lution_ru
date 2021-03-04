from django.urls import path

from . import views

urlpatterns = [
    path('blogs', views.BlogView.as_view()),
    path('registration', views.registration),
    path('', views.TopicListView.as_view(), name='index.html'),
]
