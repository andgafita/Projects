import requests
import re
import json

BASE_URL = r'https://www.info.uaic.ro/announcement_student/'


def get_announcements_fii():
    print("Anunturi fii")
    # response = requests.get(BASE_URL, verify=False)
    # data = response.text
    # create_date_anon(data)
    # pages = re.findall(r'class=page-numbers href=([^>]+)>', data)
    # for page in pages:
    #     response = requests.get(page, verify=False)
    #     data = response.text
    #     create_date_anon(data)


def create_date_anon(data):
    dates = re.findall(r'pubdate>([^<]+)</time>', data)
    anouncements = re.findall(r'href=([^ ]+) title="[^"]+"', data)
    date_anon = list(zip(dates, anouncements))
    # print(date_anon)
    for item in date_anon:
        response_json = create_json(item)
        # print(response_json)
        with open("./jsons/{}".format(response_json["title"]), "w", encoding='utf-8') as f:
            json.dump(response_json, f, indent=4, ensure_ascii=False)
        f.close()


def create_json(item):

    final_dict = {"date": item[0], 'source': 'FII'}
    response = requests.get(item[1], verify=False)
    data = response.text
    # print(type(data))
    title = re.search(r'<title>([^<]+)</title>', data)
    title = title.group(1).split(' ')[:-3]
    title = ' '.join(title)
    if "&#8211;" in title:
        title = title.replace("&#8211;", "")
    content = re.search(r'<p>([^$]+)(\.</p><div|</li></ul><div)', data)
    content = content.group(1)
    # print(content)
    final_dict["title"] = title
    final_dict["content"] = content

    return final_dict



get_announcements_fii()