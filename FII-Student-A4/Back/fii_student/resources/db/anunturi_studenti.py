import requests
import re
import json
import datetime

URLS = [r'https://www.info.uaic.ro/regulamente/', r'https://www.info.uaic.ro/documente-formulare/',
        r'https://www.info.uaic.ro/contact/']
# BASE_URL = r'https://www.info.uaic.ro/regulamente/'
for url in URLS:
    response = requests.get(url, verify=False)
    data = response.text

    final_dict = {}

    final_dict['date'] = str(datetime.datetime.now())
    final_dict['title'] = re.search(r'class="post-title">([^<]+)<', data).group(1)
    final_dict['content'] = re.search(r'(<div\s*class=post-content>[^$]+?</div>)', data).group(1)
    final_dict['type'] = 'internal'

    with open("./jsons/{}".format(final_dict["title"]), "w", encoding='utf-8') as f:
        json.dump(final_dict, f, indent=4, ensure_ascii=False)
    f.close()

print(final_dict)


