from django.urls import path

from .views import *

urlpatterns = [
    path(r'', show_news, name='news_show'),

    path('add_news/', add_news, name='add_news'),
    path('<news_id>/', NewsDetail.as_view(), name='news-detail'),
]