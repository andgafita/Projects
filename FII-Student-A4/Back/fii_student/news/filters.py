from .models import News
import django_filters
import django.forms


class NewsFilter(django_filters.FilterSet):
    # Filtrare dupa campurile din personalise
    # trimit o data toate datele pentru butonul de (toate anunturile)
    # si o data datele filtrate
    class Meta:
        model = News
        fields = []

