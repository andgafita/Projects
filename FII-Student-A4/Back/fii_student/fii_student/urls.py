"""fii_student URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from api.views import *
from api.serializers import *
from fii_student import views as fii_student_views


router = routers.DefaultRouter()
router.register('news', NewsViewSet)
router.register('boards', BoardViewSet)
router.register('cards', CardsViewSet)
router.register('resources', ResourcesViewSet)
router.register('orar', OrarViewSet)
router.register('personalise', PersonaliseViewSet)

urlpatterns = [
    path('', fii_student_views.show_landing_page, name='show_landing_page'),
    path('prezentare', fii_student_views.show_prezentare_page, name='show_prezentare_page'),
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('personalise/', include('personalise.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', include('users.urls')),
    path('orar/', include('orar.urls')),
    path('resources/', include('resources.urls')),
    path('3d_tour/', include('3d_tour.urls'))
]
