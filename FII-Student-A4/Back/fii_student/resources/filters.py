from .models import Resources
import django_filters
import django.forms


class ResourcesFilter(django_filters.FilterSet):

    class Meta:
        model = Resources
        fields = []

