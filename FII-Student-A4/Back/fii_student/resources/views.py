from builtins import super

from .models import Resources
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from pprint import pprint


@login_required(login_url='/')
def show_resources(request):
    post_url = reverse('resources_show')
    generic_objects = Resources.objects.all()
    generic_types = Resources.objects.order_by().values('type').distinct()
    # filtered_objects = generic_objects
    # filtered = table = None
    #
    # filtered = NewsFilter(request.GET, queryset=generic_objects)
    # filtered_objects = filtered.qs
    #
    # table = NewsTable(filtered_objects)
    # RequestConfig(request, paginate={"per_page": 25}).configure(table)
    #
    # tdelta = sum((float(i['time']) for i in connection.queries))
    # setattr(table, 'tdelta', tdelta)
    return render(request, 'show_resources.html',
                  {'title': 'Resources',
                   'post_url_name': 'resources_show',
                   'post_url': post_url,
                   'objects': generic_objects,
                   'types' : generic_types
                   # 'filter': filtered,
                   })

class ResourceDetail(DetailView):
    model = Resources
    # post_url = reverse('news-detail')
    template_name = "resource-individual.html"
    pk_url_kwarg = 'resources_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context
