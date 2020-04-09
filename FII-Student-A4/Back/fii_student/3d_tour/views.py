from builtins import super
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from pprint import pprint


@login_required(login_url='/')
def show_3d_scheme(request):

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
    return render(request, '3d_scheme.html')

# class ResourceDetail(DetailView):
#     model = Resources
#     # post_url = reverse('news-detail')
#     template_name = "resource-individual.html"
#     pk_url_kwarg = 'resources_id'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['now'] = timezone.now()
#         return context
