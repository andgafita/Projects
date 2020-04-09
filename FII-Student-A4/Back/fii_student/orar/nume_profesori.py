import requests
import re
import json

ORAR_URL = r"https://profs.info.uaic.ro/~orar/orar_profesori.html"

def generate_nume():

    request = requests.get(ORAR_URL)
    data = request.text
    site_title = re.findall(r'<li><a href="[^"]+">\s*([^<]+)</a>', data)
    final_list = []
    for item in site_title:
        item = item.split(',')[0]
        item = re.sub(r'\r\n', '', item).strip()
        final_list.append(item)

    with open(r'./orare/nume_profesori', 'w') as f:
        json.dump(final_list, f, indent=4)
    f.close()

generate_nume()