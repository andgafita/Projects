from django.shortcuts import render
from django.urls import reverse


def show_landing_page(request):

    if request.user.is_authenticated :
        return render(request, 'prezentare.html',
                  {'title': 'MainPage',
                   'post_url_name': 'show_main_page',
                   })
    else:
        return render(request, 'prezentare.html',
                  {'title': 'MainPage',
                   'post_url_name': 'show_main_page',
                   })

def show_prezentare_page(request):
    return render(request, 'prezentare_proiect.html',
                  {'title': 'MainPage',
                   'post_url_name': 'show_main_page',
                   })