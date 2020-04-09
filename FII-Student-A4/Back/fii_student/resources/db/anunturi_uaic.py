import requests
import re
import json
import datetime
from bs4 import BeautifulSoup

URLS = [r'http://www.uaic.ro/studenti/ghidul-studentului-uaic/',
        r'http://www.uaic.ro/studenti/burse/',
        r'http://www.uaic.ro/studenti/cazare/',
        r'http://www.uaic.ro/studenti/cantinele-universitatii-alexandru-ioan-cuza/',
        r'http://www.uaic.ro/studenti/mobilitati-academice-pentru-studenti/',
        r'http://www.uaic.ro/studenti/reprezentarea-studentilor-structurile-de-conducere-2/',
        r'http://www.uaic.ro/studenti/cariera/',
        r'http://www.uaic.ro/studenti/asociatii-si-ligi-studentesti/',
        r'http://www.uaic.ro/studenti/cum-iti-poti-verifica-notele/',
        r'http://www.uaic.ro/studenti/accesul-la-internet/',
        r'http://www.uaic.ro/studenti/servicii-de-email-pentru-studentii-uaic/',
        r'http://www.uaic.ro/studenti/servicii-medicale/',
        r'http://www.uaic.ro/studenti/regulamente/',
        r'http://www.uaic.ro/studenti/biblioteci/',
        r'http://www.uaic.ro/iasi/'
        ]
# BASE_URL = r'https://www.info.uaic.ro/regulamente/'
for url in URLS:
    response = requests.get(url, verify=False)
    data = response.text
    # print(url.rsplit('/')[-2])
    final_dict = {}

    final_dict['date'] = str(datetime.datetime.now())
    final_dict['title'] = url.rsplit('/')[-2]
    soup = BeautifulSoup(data, features="lxml")
    final_dict['content'] = soup.findAll("body")[0].renderContents().decode('utf-8')
    final_dict['type'] = 'external'

    with open("./jsons/{}".format(final_dict["title"]), "w", encoding='utf-8') as f:
        json.dump(final_dict, f, indent=4, ensure_ascii=False)
    f.close()

print(final_dict)
