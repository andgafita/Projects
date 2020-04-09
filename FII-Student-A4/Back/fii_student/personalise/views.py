import simplejson as simplejson
from django.http import HttpResponse, Http404

from .models import Personalise, Board, PersonaliseOrar, Cards
from users.models import FiiUser
from .forms import BoardForm
from .forms import NotificationForm
from .models import Board
from resources.models import Resources
from .models import Notification
from .models import dict_ani_studiu
from orar.models import Rand
from orar.views import *
from utils import generics
from django.shortcuts import render, redirect, get_object_or_404
from django_tables2 import RequestConfig, tables
from django.urls import reverse
from django.db import connection
from django.views.generic import DetailView
from news.models import News

import os


@login_required(login_url='/')
def show_personalise(request):
    post_url = reverse('personalise_show')
    generic_objects = Personalise.objects.all()
    # filtered_objects = generic_objects
    # filtered = None
    #
    # filtered = NewsFilter(request.GET, queryset=generic_objects)
    # filtered_objects = filtered.qs
    #
    # tdelta = sum((float(i['time']) for i in connection.queries))
    # setattr(table, 'tdelta', tdelta)
    return render(request, 'show_personalise.html',
                  {'title': 'Personalise',
                   'post_url_name': 'personalise_show',
                   'post_url': post_url,
                   'objects': generic_objects,
                   # 'filtered_objects': filtered,
                   })


@login_required(login_url='/')
def show_join_board(request):
    post_url = reverse('join_board_show')
    generic_objects = Board.objects.all()

    return render(request, 'join_board.html',
                  {'title': 'Board',
                   'post_url_name': 'join_board',
                   'post_url': post_url,
                   'boards': generic_objects,
                   # 'filtered_objects': filtered,
                   })


@login_required(login_url='/')
def add_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.save()
            return redirect('/personalise/boards')
    else:
        form = BoardForm()
    return render(request, 'add_board.html', {'form': form})


def add_pref_board(request, uid, bid):
    data = {
        'status': 'False'
    }
    if request.method == 'POST':
        try:
            user = get_object_or_404(FiiUser, pk=uid)
            board = get_object_or_404(Board, pk=bid)
            if user and board:
                if not user.personalise:
                    p = Personalise()
                    p.save()
                    p.init_orar(user.an_studiu, user.grupa)
                    user.personalise = p
                    user.save()
                user.personalise.add_board(board)
                data['status'] = 'True'
        except Http404:
            data['message'] = 'Invalid user or board!'
    serialized_data = simplejson.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')


def remove_pref_board(request, uid, bid):
    data = {
        'status': 'False'
    }
    if request.method == 'POST':
        try:
            user = get_object_or_404(FiiUser, pk=uid)
            board = get_object_or_404(Board, pk=bid)
            if user and board:
                if user.personalise:
                    user.personalise.remove_board(board)
                    data['status'] = 'True'
        except Http404:
            data['message'] = 'Invalid user or board!'
    serialized_data = simplejson.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')


def check_joined_board(request, uid, bid):
    data = {
        'status': 'False'
    }
    try:
        user = get_object_or_404(FiiUser, pk=uid)
        board = get_object_or_404(Board, pk=bid)
        if user and board:
            if user.personalise and user.personalise.check_has_board(board):
                data['status'] = 'True'
    except Http404:
        data['message'] = 'Invalid board or user!'

    serialized_data = simplejson.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')


def check_joined_boards(request, uid):
    data = {
        'boards': []
    }
    try:
        user = get_object_or_404(FiiUser, pk=uid)
        if user:
            if user.personalise:
                data['boards'] = [str(board.id) for board in user.personalise.boards.all()]
    except Http404:
        data['message'] = 'Invalid user!'

    serialized_data = simplejson.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')


class BoardDetail(DetailView):
    model = Board
    # post_url = reverse('news-detail')
    template_name = "board-individual.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context

@login_required(login_url='/')
def show_orar(request):
    if '?' not in request.get_raw_uri():
        _query = ''
        if request.user.rol == 'Student' or request.user.rol == 'Masterand':
            anul_userului = 0
            if (request.user.an_studiu == 'I'):
                anul_userului = 1
            elif (request.user.an_studiu == 'II'):
                anul_userului = 2
            elif (request.user.an_studiu == 'III'):
                anul_userului = 3
            else:
                anul_userului = 1
        if request.user.rol == 'Student':
            _query = "/personalise/orar/?grupa=I" + str(anul_userului) + request.user.grupa
        elif request.user.rol == 'Masterand':
            _query = "/personalise/orar/?grupa=" + request.user.grupa + str(anul_userului)
        elif request.user.rol == 'Doctorand' or request.user.rol == '-':
            _query = "/personalise/orar/?grupa=I1A1"
        elif request.user.rol == 'Profesor':
            first_name = request.user.first_name
            last_name = request.user.last_name
            nume_din_lista_profesori = cauta_nume_profesor(first_name,last_name)
            _query = "/personalise/orar/?profesor=" + nume_din_lista_profesori

        return redirect(_query)

    grupe = []
    _grupe_queryset = Rand.objects.all().values_list('grupa').distinct()
    for gr in _grupe_queryset:
        grupe.append(gr[0])
    _grupe_set = {'I1'}
    for gr in grupe:
        for aux in gr.split(','):
            _grupe_set.add(aux)
    _grupe_set.remove('')
    lista_grupe = sorted(_grupe_set)

    print(datetime.datetime.now().strftime("%A"))
    randuri = Rand.objects.all()
    titlu = ""

    if "sali_libere_acum" in request.GET:
        day = datetime.datetime.now().strftime("%A")
        if day == "Monday":
            day = "Luni"
        if day == "Tuesday":
            day = "Marti"
        if day == "Wednesday":
            day = "Miercuri"
        if day == "Thursday":
            day = "Joi"
        if day == "Friday":
            day = "Vineri"
        if day == "Saturday":
            day = "Sambata"
        if day == "Sunday":
            day = "Duminica"
        time_hour = datetime.datetime.now().time()
        randuri = randuri.exclude(zi__contains=',')
        sali_ocupate = Rand.objects.exclude(zi__contains=',').filter(ora_inceput__lt=time_hour, ora_sfarsit__gt=time_hour, zi=day).distinct(
            'sala')
        randuri = randuri.exclude(sala__in=sali_ocupate.values('sala')).exclude(sala = "").distinct('sala')
        print(sali_ocupate)
        template = loader.get_template('saliLibere.html')
        context = {'grupe': lista_grupe, 'sali': get_sali_unique(), 'cursuri': get_materii_unique(), 'randuri': randuri}
        return HttpResponse(template.render(context, request))
    request_materie = ""
    request_grupa = ""
    request_sala = ""
    request_profesor = ""
    if "sala" in request.GET:
        request_sala = request.GET['sala']
        if request_sala is not "":
            randuri = randuri.filter(sala__contains=request_sala)
            titlu = "Sala " + request_sala

    if "materie" in request.GET:
        request_materie = request.GET['materie']
        if request_materie is not "":
            randuri = randuri.filter(curs=request_materie)
            titlu = "Materia " + request_materie

    if "profesor" in request.GET:
        request_profesor = request.GET['profesor']
        if request_profesor is not "":
            randuri = randuri.filter(profesor__contains=request_profesor)
            titlu = "Profesor " + request_profesor
    randuri1 = randuri
    if "grupa" in request.GET:
        request_grupa = request.GET['grupa']
        if request_grupa is not "":
            grupa_len = len(request_grupa)
            randuri = randuri.filter(grupa__iregex=(r'([A-Za-z0-9]{0})' + request_grupa + r'(?![a-zA-Z0-9])')).exclude(
                    grupa__iregex=(r'[A-Za-z0-9]' + request_grupa )).distinct()
            for i in range(1, grupa_len):
                req_group = request_grupa[0:i]
                print(req_group)
                randuri = randuri | randuri1.filter(
                    grupa__iregex=(r'([A-Z0-9]{0})' + req_group + r'(?![a-zA-Z0-9])')).exclude(
                    grupa__iregex=(r'[A-Za-z0-9]' + req_group )).distinct()
            randuri = randuri | randuri1.filter(grupa__contains=request_grupa).distinct()
            if request_grupa == 'I1' or request_grupa == 'I2':
                randuri.exclude(grupa__contains='MSI')
            titlu = "Grupa " + request_grupa

    randuri = randuri.distinct('curs','ora_inceput','ora_sfarsit','profesor','sala','tip','zi')
    randuri_totale = randuri.order_by('ora_inceput')
    randuri_examen = randuri_totale.filter(zi__contains=',')
    #randuri_examen = randuri_totale.filter(tip = 'Examen')
    #randuri_examen = randuri_examen | randuri_totale.filter(tip = 'Restante')#randurile pentru examene
    randuri = randuri_totale.exclude(zi__contains=',') #randurile pentru orarul propriu-zis
    luni = randuri.filter(zi='Luni')
    marti = randuri.filter(zi='Marti')
    miercuri = randuri.filter(zi='Miercuri')
    joi = randuri.filter(zi='Joi')
    vineri = randuri.filter(zi='Vineri')
    sambata = randuri.filter(zi='Sambata')
    duminica = randuri.filter(zi='Duminica')
    zile_examene = get_zile_examene(randuri_examen)
    zile_saptamana_examene = get_zile_saptamana_examene(zile_examene,randuri_examen)

    template = loader.get_template('orar.html')
    list = []

    list.append(calculate_sum(luni))
    list.append(calculate_sum(marti))
    list.append(calculate_sum(miercuri))
    list.append(calculate_sum(joi))
    list.append(calculate_sum(vineri))
    list.append(calculate_sum(sambata))
    list.append(calculate_sum(duminica))

    # grupe = Rand.objects.all().values('grupa').exclude(grupa__contains=',').distinct()
    # print(Rand.objects.values('sala').distinct())

    context = {'grupe': lista_grupe, 'sali': get_sali_unique(), 'cursuri': get_materii_unique(),'profesori': get_profesori_unique(), 'lista_ore': list,
               'titlu': titlu, 'luni': luni, 'marti': marti, 'miercuri': miercuri, 'joi': joi, 'vineri': vineri,
               'sambata': sambata, 'duminica': duminica,'SALAH': request_sala,"GRUPAH": request_grupa, "MATERIAH": request_materie,'PROFESORH':request_profesor,'zile_examen':zile_examene,'examene':randuri_examen,'zile_saptamana_examene':zile_saptamana_examene}

    return HttpResponse(template.render(context, request))


def add_rand(request, uid, rid):
    data = {
        'status': 'False'
    }
    if request.method == 'POST':
        try:
            user = get_object_or_404(FiiUser, pk=uid)
            rand = get_object_or_404(Rand, pk=rid)
            if user and rand:
                if not user.personalise:
                    p = Personalise()
                    p.save()
                    p.init_orar(user.an_studiu, user.grupa)
                    user.personalise = p
                    user.save()
                user.personalise.add_class(rand)
                data['status'] = 'True'
        except Http404:
            data['message'] = 'Invalid user or board!'
    serialized_data = simplejson.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')


def remove_rand(request, uid, rid):
    data = {
        'status': 'False'
    }
    if request.method == 'POST':
        try:
            user = get_object_or_404(FiiUser, pk=uid)
            rand = get_object_or_404(Rand, pk=rid)
            if user and rand:
                if user.personalise:
                    user.personalise.remove_class(rand)
                    data['status'] = 'True'
        except Http404:
            data['message'] = 'Invalid user or board!'
    serialized_data = simplejson.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')


def check_rands(request, uid):
    data = {
        'rands': []
    }
    try:
        user = get_object_or_404(FiiUser, pk=uid)
        if user:
            if user.personalise:
                data['rands'] = [str(rand.rand_id) for rand in PersonaliseOrar.objects.filter(personalise=user.personalise)]
    except Http404:
        data['message'] = 'Invalid user!'

    serialized_data = simplejson.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')


def show_orar_personalised(request):
    grupe = []
    _grupe_queryset = Rand.objects.all().values_list('grupa').distinct()
    for gr in _grupe_queryset:
        grupe.append(gr[0])
    _grupe_set = {'I1A1'}
    _grupe_set.add('MIS1')
    _grupe_set.add('MSI')
    for gr in grupe:
        for aux in gr.split(','):
            _grupe_set.add(aux)
    _grupe_set.remove('')
    lista_grupe = sorted(_grupe_set)

    print(datetime.datetime.now().strftime("%A"))
    ids = [ora.rand_id for ora in PersonaliseOrar.objects.filter(personalise = request.user.personalise)]		
    randuri = Rand.objects.filter(id__in=ids)
    titlu = ""

    if "sali_libere_acum" in request.GET:
        day = datetime.datetime.now().strftime("%A")
        if day == "Monday":
            day = "Luni"
        if day == "Tuesday":
            day = "Marti"
        if day == "Wednesday":
            day = "Miercuri"
        if day == "Thursday":
            day = "Joi"
        if day == "Friday":
            day = "Vineri"
        if day == "Saturday":
            day = "Sambata"
        if day == "Sunday":
            day = "Duminica"
        time_hour = datetime.datetime.now().time()
        randuri = randuri.exclude(zi__contains=',')
        sali_ocupate = Rand.objects.exclude(zi__contains=',').filter(ora_inceput__lt=time_hour, ora_sfarsit__gt=time_hour, zi=day).distinct(
            'sala')
        randuri = randuri.exclude(sala__in=sali_ocupate.values('sala')).exclude(sala = "").distinct('sala')
        print(sali_ocupate)
        template = loader.get_template('saliLibere.html')
        context = {'grupe': lista_grupe, 'sali': get_sali_unique(), 'cursuri': get_materii_unique(), 'randuri': randuri}
        return HttpResponse(template.render(context, request))
    request_materie = ""
    request_grupa = ""
    request_sala = ""
    request_profesor = ""
    if "sala" in request.GET:
        request_sala = request.GET['sala']
        if request_sala is not "":
            randuri = randuri.filter(sala__contains=request_sala)
            titlu = "Sala " + request_sala

    if "materie" in request.GET:
        request_materie = request.GET['materie']
        if request_materie is not "":
            randuri = randuri.filter(curs=request_materie)
            titlu = "Materia " + request_materie

    if "profesor" in request.GET:
        request_profesor = request.GET['profesor']
        if request_profesor is not "":
            randuri = randuri.filter(profesor__contains=request_profesor)
            titlu = "Profesor " + request_profesor
    randuri1 = randuri
    if "grupa" in request.GET:
        request_grupa = request.GET['grupa']
        if request_grupa is not "":
            grupa_len = len(request_grupa)
            randuri = randuri.filter(grupa__iregex=(r'([A-Za-z0-9]{0})' + request_grupa + r'(?![a-zA-Z0-9])')).exclude(
                    grupa__iregex=(r'[A-Za-z0-9]' + request_grupa )).distinct()
            for i in range(1, grupa_len):
                req_group = request_grupa[0:i]
                print(req_group)
                randuri = randuri | randuri1.filter(
                    grupa__iregex=(r'([A-Z0-9]{0})' + req_group + r'(?![a-zA-Z0-9])')).exclude(
                    grupa__iregex=(r'[A-Za-z0-9]' + req_group )).distinct()
            randuri = randuri | randuri1.filter(grupa__contains=request_grupa).distinct()
            if request_grupa == 'I1' or request_grupa == 'I2':
                randuri.exclude(grupa__contains='MSI')
            titlu = "Grupa " + request_grupa

    randuri = randuri.distinct('curs','ora_inceput','ora_sfarsit','profesor','sala','tip','zi')
    randuri_totale = randuri.order_by('ora_inceput')
    randuri_examen = randuri_totale.filter(zi__contains=',')
    #randuri_examen = randuri_totale.filter(tip = 'Examen')
    #randuri_examen = randuri_examen | randuri_totale.filter(tip = 'Restante')#randurile pentru examene
    randuri = randuri_totale.exclude(zi__contains=',') #randurile pentru orarul propriu-zis
    luni = randuri.filter(zi='Luni')
    marti = randuri.filter(zi='Marti')
    miercuri = randuri.filter(zi='Miercuri')
    joi = randuri.filter(zi='Joi')
    vineri = randuri.filter(zi='Vineri')
    sambata = randuri.filter(zi='Sambata')
    duminica = randuri.filter(zi='Duminica')
    zile_examene = get_zile_examene(randuri_examen)
    zile_saptamana_examene = get_zile_saptamana_examene(zile_examene,randuri_examen)

    template = loader.get_template('orar.html')
    list = []

    list.append(calculate_sum(luni))
    list.append(calculate_sum(marti))
    list.append(calculate_sum(miercuri))
    list.append(calculate_sum(joi))
    list.append(calculate_sum(vineri))
    list.append(calculate_sum(sambata))
    list.append(calculate_sum(duminica))

    # grupe = Rand.objects.all().values('grupa').exclude(grupa__contains=',').distinct()
    # print(Rand.objects.values('sala').distinct())

    context = {'grupe': lista_grupe, 'sali': get_sali_unique(), 'cursuri': get_materii_unique(),'profesori': get_profesori_unique(), 'lista_ore': list,
               'titlu': titlu, 'luni': luni, 'marti': marti, 'miercuri': miercuri, 'joi': joi, 'vineri': vineri,
               'sambata': sambata, 'duminica': duminica,'SALAH': request_sala,"GRUPAH": request_grupa, "MATERIAH": request_materie,'PROFESORH':request_profesor,'zile_examen':zile_examene,'examene':randuri_examen,'zile_saptamana_examene':zile_saptamana_examene}

    return HttpResponse(template.render(context, request))


def reset_orar(request):
    request.user.personalise.init_orar(request.user.an_studiu, request.user.grupa)
    return redirect('../')


def get_cards(request):
    data = [{}]
    if request.user.is_authenticated:
        user = request.user
        cards = Cards.objects.filter(personalise=user.personalise)
        for card in cards:
            if card.is_valid():
                json = card.getJSON()
                data.append(json)
    serialized_data = simplejson.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')


def add_card(request):
    data = {
        'Status': 'Fail'
    }
    if request.user.is_authenticated and request.method == 'POST':
        try:
            x = request.POST['x']
            y = request.POST['y']
            width = request.POST['width']
            height = request.POST['height']
            type = request.POST['type']
            card = Cards(personalise_id=request.user.personalise_id, x=int(x), y=int(y), width=int(width), height=int(height), type=type)
            card.save()
            data['Status'] = 'Success'
            data['id'] = card.id
        except:
            data['Status'] = 'Fail'
    serialized_data = simplejson.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')


def remove_card(request, cid):
    data = {
        'Status': 'Fail'
    }
    if request.user.is_authenticated and request.method == 'POST':
        try:
            card = get_object_or_404(Cards, pk=cid)
            card.delete()
            data['Status'] = 'Success'
        except Http404:
            data['Status'] = 'Fail'
            data['message'] = 'Invalid card id'
        except:
            data['Status'] = 'Fail'
        serialized_data = simplejson.dumps(data)
        return HttpResponse(serialized_data, content_type='application/json')


def update_card(request, cid):
    data = {
        'Status': 'Fail'
    }
    if request.user.is_authenticated and request.method == 'POST':
        try:
            card = get_object_or_404(Cards, pk=cid)
            x = request.POST['x']
            y = request.POST['y']
            width = request.POST['width']
            height = request.POST['height']
            card.x = int(x)
            card.y = int(y)
            card.width = int(width)
            card.height = int(height)
            card.save()
            data['Status'] = 'Success'
        except:
            data['Status'] = 'Fail'
    serialized_data = simplejson.dumps(data)
    return HttpResponse(serialized_data, content_type='application/json')


@login_required(login_url='/')
def show_notificari(request):
    notifications = Notification.objects.filter(personalise=request.user.personalise)
    boards = Board.objects.none()
    news = News.objects.none()
    resources = Resources.objects.none()
    for notification in notifications:
        if notification.category == 'Boards':
            boards |= Board.objects.filter(subject__icontains=notification.keyword) | Board.objects.filter(teacher__icontains=notification.keyword) | Board.objects.filter(description__icontains=notification.keyword)
        if notification.category == 'Noutati':
            news |= News.objects.filter(title__icontains=notification.keyword) | News.objects.filter(author_name__icontains=notification.keyword) | News.objects.filter(category__icontains=notification.keyword) | News.objects.filter(body__icontains=notification.keyword)
        if notification.category == 'Resurse':
            resources |= Resources.objects.filter(title__icontains=notification.keyword) | Resources.objects.filter(content__icontains=notification.keyword) | Resources.objects.filter(type__icontains=notification.keyword)
    boards = boards.order_by('year')
    news = news.order_by('inserted_time')
    resources = resources.order_by('timestamp')
    if request.user.is_authenticated and request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = Notification(personalise_id=request.user.personalise_id, category=request.POST['category'], keyword=request.POST['keyword'])
            notification.save()
            return redirect('/personalise/notificari')
    else:
        form = NotificationForm()
    context = {'form': form, 'notifications' : notifications, 'boards' : boards, 'news': news, 'resources' : resources}
    return render(request, 'notificari.html', context)

def remove_notification(request, id):
    if request.user.is_authenticated:
        notification = get_object_or_404(Notification, id=id)
        notification.delete()
    return redirect('/personalise/notificari')
