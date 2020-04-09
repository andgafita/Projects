from django.urls import re_path,path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'program_sali/$',views.program_sali,name = 'program_sali'),
]