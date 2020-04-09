from django.urls import path

from .views import *

urlpatterns = [
    path(r'', show_3d_scheme, name='3d_scheme_show')]
