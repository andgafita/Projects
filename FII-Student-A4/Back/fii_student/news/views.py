from news.forms import NewsForm
from .models import News
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
import datetime
from dateutil.relativedelta import relativedelta
import re


@login_required(login_url='/')
def show_news(request):
    post_url = reverse('news_show')
    generic_objects = News.objects.all()

    # for object in generic_objects:
    #     object.body.replace('/bin', 'https://www.info.uaic.ro/bin')
    #     #object.body.replace('127.0.0.1:8000', 'https://www.info.uaic.ro')
    #     object.save()

    # for object in generic_objects:
    #     result=re.findall('<img (.)+>', object.body);
    #     print(result);
    # print(request)
    # print(request.read())
    # filtered_objects = generic_objects
    # filtered = None
    #
    # filtered = NewsFilter(request.GET, queryset=generic_objects)
    # filtered_objects = filtered.qs
    #
    # tdelta = sum((float(i['time']) for i in connection.queries))
    # setattr(table, 'tdelta', tdelta)
    return render(request, 'show_news.html',
                  {'title': 'News',
                   'post_url_name': 'news_show',
                   'post_url': post_url,
                   'objects': generic_objects,
                   # 'filtered_objects': filtered,
                   })


# @login_required(login_url='/')
class NewsDetail(DetailView):
    model = News
    # post_url = reverse('news-detail')
    template_name = "anunturi-individual.html"
    pk_url_kwarg = 'news_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context


@login_required(login_url='/')
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            pieceOfNews = form.save(commit=False)
            pieceOfNews.source="FII"
            if request.user.is_authenticated:
                pieceOfNews.author_name=request.user.first_name + ' ' + request.user.last_name
            else:
                pieceOfNews.author_name='Anonymous'
            pieceOfNews.inserted_time=datetime.datetime.now();
            pieceOfNews.published_time = datetime.datetime.now();
            pieceOfNews.expire_time = datetime.datetime.now()+relativedelta(years=1);
            pieceOfNews.save()
            return redirect('/news')
    else:
        form = NewsForm()
    return render(request, 'add_news.html', {'form': form})
