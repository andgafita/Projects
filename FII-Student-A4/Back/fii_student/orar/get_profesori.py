import requests
import json
import re
from lxml.html import fromstring


BASE_URL = r"https://profs.info.uaic.ro/~orar/"
ORAR_URL = r"https://profs.info.uaic.ro/~orar/orar_studenti.html"


def generate_orare():

    request = requests.get(ORAR_URL)
    data = request.text
    site_title = re.findall(r'<ul>\s*<li><a href="([^"]+)">([^<]+)</a></li>', data)
    # print(site_title)
    # site_title = [BASE_URL + x[0] for x in site_title]
    for item in site_title:
        item = list(item)
        item[0] = BASE_URL + item[0]
        get_orare(item[0], item[1])


# print(site_title)
# print(site_title)

def get_orare(site, title):

    print(site)
    r = requests.get(site)
    # print(r.text)
    page = fromstring(r.text)
    # print(page)

    rows = page.xpath("body/table")[0].findall("tr")
    data = list()
    for row in rows:
        data.append([c.text_content() for c in row.getchildren()])

    # print(data)

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
        if y[i][0].split(' ')[0] in days:
            index.append(i)
    index.append(len(y))
    all_days = []
    for i in range(len(index) - 1):
        all_day = []
        for j in range(index[i], index[i + 1]):
            all_day.append(y[j])
        all_days.append(all_day)
    # print(index)
    # print(all_days)

    # final_dict = {}
    # final_dict['title'] = title
    all_subjects = []
    counter = 1
    for item in all_days:
        # print(item)

        # day_dict['zi'] = item[0][0].split(' ')[0]
        # item[0][0]
        for i in range(1, len(item)):
            day_dict = {}
            subject_dict = {}
            day_dict['model'] = "orar.Rand"
            day_dict['pk'] = counter

            day_dict['fields'] = subject_dict

            counter = counter + 1
            # print(len(item[i]))
            if len(item[i]) == 9:

                subject_dict['ora_inceput'] = item[i][0]
                subject_dict['ora_sfarsit'] = item[i][1]
                subject_dict['grupa'] = re.sub(r'\s+', '', item[i][2])
                subject_dict['curs'] = item[i][3]
                subject_dict['tip'] = item[i][4]
                subject_dict['profesor'] = re.sub('\s+', ' ', item[i][5]).strip()
                subject_dict['sala'] = re.sub('\s+', ' ', item[i][6]).strip()
                # subject_dict['frecventa'] = item[i][7]
                subject_dict['pachet'] = item[i][8]
                subject_dict['zi'] = item[0][0].split(' ')[0]
            else:
                subject_dict['ora_inceput'] = item[i][0]
                subject_dict['ora_sfarsit'] = item[i][1]
                subject_dict['grupa'] = site.split('_')[1].split('.')[0]
                subject_dict['curs'] = item[i][2]
                subject_dict['tip'] = item[i][3]
                subject_dict['profesor'] = re.sub('\s+', ' ', item[i][4]).strip()
                subject_dict['sala'] = re.sub('\s+', ' ', item[i][5]).strip()
                # subject_dict['frecventa'] = item[i][6]
                subject_dict['pachet'] = item[i][7]
                subject_dict['zi'] = item[0][0].split(' ')[0]
            # print(subject_dict)
            # print("aici")
            # print(day_dict)
            # print("dupa")
            all_subjects.append(day_dict)
            # day_dict['materie {}'.format(i)] = subject_dict
        # final_dict['ore {}'.format(item[0][0].split(' ')[0])] = day_dict

        # print(day_dict)

    print(all_subjects)
    with open(r'./orare/{}'.format(title), 'w') as f:
        json.dump(all_subjects, f, indent=4)
    f.close()

generate_orare()