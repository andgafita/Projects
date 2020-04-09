from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('activation_email_sent/', activation_email_sent, name='activation_email_sent'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('logout/', logout_view, name='logout'),
    path('settings/', settings, name='settings'),
    path('settings/reset_settings/<int:uid>', reset_settings, name='reset_settings'),
    path('settings/password_change', password_change, name='password_change')
    # path('settings/password_changed', password_changed, name='password_changed')
]
