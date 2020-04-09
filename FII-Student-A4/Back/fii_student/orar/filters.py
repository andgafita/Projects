import django_filters
from .models import Rand

class RanduriFilter(django_filters.FilterSet):

    listaMaterii=Rand.objects.value('curs')

    materii=django_filters.ChoiceFilter(label='Materii',choices=listaMaterii, method='filter_materii')

    class Meta:
        model=Rand
        fields = []
    def filter_materii(self,queryset,name,value):
        pass
