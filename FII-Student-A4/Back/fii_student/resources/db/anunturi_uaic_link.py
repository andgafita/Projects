import requests
import re
import json
import datetime

# BASE_URL = r'https://www.info.uaic.ro/regulamente/'
url = r'https://www.info.uaic.ro/'
response = requests.get(url, verify=False)
data = response.text
item = re.search(r'(<li\s*id=menu-item-836[^$]+?-1926">)', data).group(1)
# print(url.rsplit('/')[-2])
lista = re.findall(r'href=(http:[^>]+)>([^<]+)</a>', item)

for it in lista:

    final_dict = {}
    final_dict['date'] = str(datetime.datetime.now())
    final_dict['site'] = it[0]
    final_dict['title'] = it[1]
    final_dict['type'] = 'external'

    with open("./jsons/{}".format(final_dict["title"]), "w", encoding='utf-8') as f:
        json.dump(final_dict, f, indent=4, ensure_ascii=False)
    f.close()

# print(final_dict)
