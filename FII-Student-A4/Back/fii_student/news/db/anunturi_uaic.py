import requests
import json
import re
counter = 1

def get_announcements_uaic():
    print("Anunturi uaic")

    # for i in range(1, 11):
    #     url = r'http://www.uaic.ro/noutati-si-comunicate/page/{}/'.format(i)
    #     r = requests.get(url)
    #     response = r.text
    #     parse_anons(response)


def parse_anons(response):

    all_links = re.findall(r'post-title"><a\s*href="([^"]+)"', response)
    for link in all_links:
        parse_anon(link)


def parse_anon(link):
    print(link)
    global counter
    r = requests.get(link)
    response = r.text

    try:
        title = re.search(r'<h1\s*class="entry-title">([^<]+)</h1>', response).group(1)
    except:
        print(link)
        return
    author = re.search(r'rel="author">([^<]+)</a><', response).group(1)
    date = re.search(r'</span><span>([^<]+)</span><span', response).group(1)
    content = re.search(r'<div\s*class="post-content">\s*([^$]+)</p>', response).group(1)

    dictionar = {}
    dictionar['source'] = "UAIC"
    dictionar['title'] = title
    dictionar['author'] = author
    dictionar['date'] = date
    dictionar['content'] = content

    with open(r'./jsons/{}.json'.format(counter), 'w', encoding='utf-8') as f:
        json.dump(dictionar, f, indent=4, ensure_ascii=False)
    f.close()
    counter = counter + 1


# get_announcements_uaic()