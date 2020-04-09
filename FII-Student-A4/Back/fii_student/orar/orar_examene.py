import requests
import json
import re
from lxml.html import fromstring


BASE_URL = r"https://profs.info.uaic.ro/~orar/"
ORAR_URL = r"https://profs.info.uaic.ro/~orar/orar_studenti.html"

counter = 1
final_list = []

def generate_orare():

    global final_list
    request = requests.get(ORAR_URL)
    data = request.text
    # site_title = re.findall(r'<ul>\s*<li><a href="([^"]+)">([^<]+)</a></li>', data)

    site_title = [
        ('participanti/orar_MIS.html', 'Master ingineria sistemelor soft'),
        ('participanti/orar_MLC.html', 'Master lingvistica computationala'),
        ('participanti/orar_MOC.html', 'Master optimizare computationala'),
        ('participanti/orar_MSD.html', 'Master sisteme distribuite'),
        ('participanti/orar_MSI.html', 'Master securitatea informatiei'),
        ('participanti/orar_I1.html', 'Informatica, anul 1'),
        ('participanti/orar_I1X1.html', 'Cursanti, anul 1, grupa 1'),
        ('participanti/orar_I1X2.html', 'Cursanti, anul 1, grupa 2'),
        ('participanti/orar_I1X3.html', 'Cursanti, anul 1, grupa 3'),
        ('participanti/orar_I1X4.html', 'Cursanti, anul 1, grupa 4'),
        ('participanti/orar_I1X5.html', 'Cursanti, anul 1, grupa 5'),
        ('participanti/orar_I2.html', 'Informatica, anul 2'),
        ('participanti/orar_I2X1.html', 'Reinmatriculari, anul 2, grupa 1'),
        ('participanti/orar_I2X2.html', 'Cursanti, anul 2, grupa 2'),
        ('participanti/orar_I3.html', 'Informatica, anul 3'),
        ('participanti/orar_I3E.html', 'Informatica, anul 3 Engleza'),
        ('participanti/orar_I3X1.html', 'Reinmatriculari, anul 3')
    ]

    for item in site_title:
        item = list(item)
        item[0] = BASE_URL + item[0]
        get_orare(item[0], item[1])
    with open(r'./orare_examen/orar_examene', 'w') as f:
        json.dump(final_list, f, indent=4)
    f.close()


# print(site_title)
# print(site_title)

def get_orare(site, title):

    global counter, final_list
    print(site)
    r = requests.get(site)
    # print(r.text)
    page = fromstring(r.text)
    # print(page)
    try:
        rows = page.xpath("body/table")[1].findall("tr")
    except:
        return {}
    data = list()
    for row in rows:
        data.append([c.text_content() for c in row.getchildren()])

    print(data)

    y = []
    for row in data:
        z = []
        for item in row:
            # print(item)
            item = re.sub(r'\r\n', '', item).strip()
            z.append(item)
        y.append(z)
        # print(item)

    # print(y)

    days = ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri', 'Sambata', 'Duminica']
    index = []
    for i in range(len(y)):
        # print()
        if y[i][0].split(',')[0] in days:
            index.append(i)
    index.append(len(y))
    all_days = []
    for i in range(len(index) - 1):
        all_day = []
        for j in range(index[i], index[i + 1]):
            all_day.append(y[j])
        all_days.append(all_day)

    for item in all_days:
        for i in range(1, len(item)):
            day_dict = {}
            subject_dict = {}
            day_dict['model'] = "orar.Rand"
            day_dict['pk'] = counter

            day_dict['fields'] = subject_dict

            counter = counter + 1
            # print(len(item[i]))
            if len(item[i]) == 8:

                subject_dict['ora_inceput'] = item[i][0]
                subject_dict['ora_sfarsit'] = item[i][1]
                subject_dict['grupa'] = re.sub(r'\s+', '', item[i][2])
                subject_dict['curs'] = item[i][3]
                subject_dict['tip'] = item[i][4]
                subject_dict['profesor'] = re.sub('\s+', ' ', item[i][5]).strip()
                subject_dict['sala'] = re.sub('\s+', ' ', item[i][6]).strip()
                # subject_dict['frecventa'] = item[i][7]
                subject_dict['pachet'] = item[i][7]
                subject_dict['zi'] = item[0][0]
            else:
                subject_dict['ora_inceput'] = item[i][0]
                subject_dict['ora_sfarsit'] = item[i][1]
                subject_dict['grupa'] = site.split('_')[1].split('.')[0]
                subject_dict['curs'] = item[i][2]
                subject_dict['tip'] = item[i][3]
                subject_dict['profesor'] = re.sub('\s+', ' ', item[i][4]).strip()
                subject_dict['sala'] = re.sub('\s+', ' ', item[i][5]).strip()
                # subject_dict['frecventa'] = item[i][6]
                subject_dict['pachet'] = item[i][6]
                subject_dict['zi'] = item[0][0]
            final_list.append(day_dict)

generate_orare()