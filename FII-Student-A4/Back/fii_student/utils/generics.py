from django.shortcuts import render
from django_tables2 import RequestConfig, tables
from django.urls import reverse
from django.db import connection


def generic_show(request, title, generic_class, filter_class,
                 table_class: tables, post_url_name, per_page=25):
    post_url = reverse(post_url_name)
    if title == 'Resources':
        generic_objects = generic_class.objects.only('object_id', 'type', 'path', 'label', 'groups')
    else:
        generic_objects = generic_class.objects.all()
    filtered_objects = generic_objects
    filtered = table = None

    if filter_class is not None:
        filtered = filter_class(request.GET, queryset=generic_objects)
        filtered_objects = filtered.qs

    if table_class is not None:
        table = table_class(filtered_objects)
        RequestConfig(request, paginate={"per_page": per_page}).configure(table)


    tdelta = sum((float(i['time']) for i in connection.queries))
    setattr(table, 'tdelta', tdelta)

    return render(request, 'yoda/templates/show_table_template.html',
                  {'title': title,
                   'post_url_name': post_url_name,
                   'post_url': post_url,
                   'table': table,
                   'filter': filtered})
