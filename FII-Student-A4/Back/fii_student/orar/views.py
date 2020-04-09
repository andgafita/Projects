from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Rand
from django.shortcuts import redirect
from django.db.models import Sum
import requests
import datetime
import re
from datetime import time


def calculate_sum(queryset):
    sum = 0
    for i in queryset:
        sum += i.ora_sfarsit.hour - i.ora_inceput.hour
    return sum


def get_sali_unique():
    sali_unice = {"Acvariu"}
    toate_salile = Rand.objects.exclude(zi__contains=',')
    for sala in toate_salile:
        if sala.get_sala() is not "":
            sali_unice.add(sala.get_sala())
    return sorted(sali_unice)


def get_zile():
    randuri = Rand.objects.exclude(zi__contains=',')
    rand = {}
    rand['Luni'] = randuri.filter(zi__contains='Luni')
    rand['Marti'] = randuri.filter(zi__contains='Marti')
    rand['Miercuri'] = randuri.filter(zi__contains='Miercuri')
    rand['Joi'] = randuri.filter(zi__contains='Joi')
    rand['Vineri'] = randuri.filter(zi__contains='Vineri')
    rand['Sambata'] = randuri.filter(zi__contains='Sambata')
    rand['Duminica'] = randuri.filter(zi__contains='Duminica')
    return rand


def verificare_disp(_sala, zi, i):
    sali = zi.filter(sala=_sala)
    t_inceput = time(i)
    t_sfarsit = time(i + 1)
    for sala in sali:
        if (
                t_sfarsit <= sala.ora_sfarsit and t_sfarsit > sala.ora_inceput or t_inceput >= sala.ora_inceput and t_inceput < sala.ora_sfarsit):
            return 0
        else:
            continue
    return 1


def program_sali(request):
    zile = ["Luni", "Marti", "Miercuri", "Joi", "Vineri", "Sambata", "Duminica"]
    rand = get_zile()
    sali = get_sali_unique()
    print(sali)
    ore = [time(8), time(9), time(10), time(11), time(12), time(13), time(14), time(15), time(16), time(17), time(18),
           time(19), time(20)]
    template = loader.get_template('sali_disponibile.html')
    dict = []
    for sala in range(len(sali)):
        dict2 = []
        dict.append(dict2)
        for zi in range(0, 7):
            dict3 = []
            dict[sala].append(dict3)
            for ora in range(0, 12):
                if verificare_disp(sali[sala], rand[zile[zi]], ora + 8) == 1:
                    dict[sala][zi].append("liber")
                else:
                    dict[sala][zi].append("ocupat")

    context = {'lista': dict, 'sali': sali, 'zile': zile, 'ore': range(8, 20), 'lungime': len(sali),
               'rangesali': range(len(sali)), 'rangezile': range(7), 'rangeore': range(12)}

    return HttpResponse(template.render(context, request))

def get_profesori_unique():
    with open('./orar/orare/nume_profesori', 'r') as file:
        data = file.read().replace('\n', '')
    data=data.replace('\"','')
    data=data.replace('[','')
    data=data.replace(']','')
    data=data.replace("    ","")
    profesori=data.split(",")
    return profesori



def get_materii_unique():
    materii_unice = {"Introducere in criptografie"}
    toate_materiile = Rand.objects.all()
    for materie in toate_materiile:
        materii_unice.add(materie.get_materie())
    return sorted(materii_unice)


def compara(first_list_item,second_list_item):
    first = first_list_item.split(".")
    second = second_list_item.split(".")
    if first[2] > second[2]:
        return 1
    elif first[2] < second[2]:
        return -1
    else:
        if first[1] > second[1]:
            return 1
        elif first[1] < second[1]:
            return -1
        else:
            if first[0] > second[0]:
                return 1
            elif first[0] < second[0]:
                return -1
            else:
                return 0

def sorteaza_date(lista_date):
    list_length = len(lista_date)
    for i in range(list_length-1):
        for j in range(i+1,list_length):
            if compara(lista_date[i],lista_date[j]) == 1:
                aux = lista_date[i]
                lista_date[i] = lista_date[j]
                lista_date[j] = aux


def get_zile_examene(randuri):
    lista_date = []
    for rand in randuri:
        zi = rand.get_zi().split(", ")
        lista_date.append(zi[1])
    lista_date = list(set(lista_date))
    list_length = len(lista_date)
    for i in range(list_length - 1):
        for j in range(i + 1, list_length):
            if compara(lista_date[i], lista_date[j]) == 1:
                aux = lista_date[i]
                lista_date[i] = lista_date[j]
                lista_date[j] = aux
    return lista_date

def get_zile_saptamana_examene(zile_examene, randuri_examen):
    zile_saptamana_examene = {}
    for zi_examen in zile_examene:
        x = randuri_examen.filter(zi__contains=zi_examen)
        for zi in x:
            zile_saptamana_examene[zi_examen] = zi.get_zi()
    return zile_saptamana_examene

def cauta_nume_profesor(first_name, last_name):
    lista_nume = []
    first_name = first_name.replace('-', ' ')
    last_name = last_name.replace('-', ' ')
    for name in first_name.split():
        lista_nume.append(name)
    for name in last_name.split():
        lista_nume.append(name)
    nume_profesori = get_profesori_unique()
    aux = []
    for nume in lista_nume:
        for nume_p in nume_profesori:
            if(nume in nume_p):
                aux.append(nume_p)
        nume_profesori = aux
        aux = []
    return nume_profesori[0]

@login_required(login_url='/')
def index(request):
    if '?' not in request.get_raw_uri():
        _query = ''
        if request.user.rol == 'Student' or request.user.rol == 'Masterand':
            anul_userului = 0
            if (request.user.an_studiu == 'I'):
                anul_userului = 1
            elif (request.user.an_studiu == 'II'):
                anul_userului = 2
            elif (request.user.an_studiu == 'III'):
                anul_userului = 3;
            else:
                anul_userului = 1;
        if request.user.rol == 'Student':
            _query = "/orar/?grupa=I" + str(anul_userului) + request.user.grupa
        elif request.user.rol == 'Masterand':
            _query = "/orar/?grupa=" + request.user.grupa + str(anul_userului)
        elif request.user.rol == 'Doctorand' or request.user.rol == '-':
            _query = "/orar/?grupa=I1A1"
        elif request.user.rol == 'Profesor':
            first_name = request.user.first_name
            last_name = request.user.last_name
            nume_din_lista_profesori = cauta_nume_profesor(first_name,last_name)
            _query = "/orar/?profesor=" + nume_din_lista_profesori

        return redirect(_query)

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

    template = loader.get_template('grupa.html')
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
