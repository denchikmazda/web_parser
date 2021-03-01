from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from instituties.ivmiit import get_link_from_button
url_phys = 'https://kpfu.ru/physics'

def get_cathedras(url):
    site = urlopen(url)
    soup = bs(site, 'html.parser')

    cathedras = list()
    div = soup.find('div',class_='visit_link')
    paragraphs = div.find_all('p')
    for item in paragraphs:
        tag_a = item.find('a')
        if tag_a:
            if tag_a.text.startswith('Кафедра'):
                cathedras.append((tag_a.text, tag_a.get('href')))

    return cathedras

def get_stuff(url):
    site = urlopen(url)
    soup = bs(site,'html.parser')

    stuff = list()

    iframe = soup.find('iframe')
    if iframe:
        source = iframe.get('src')

        site = urlopen(source)
        soup = bs(site, 'html.parser')

        spans = soup.find_all('span', class_='fio')
        for item in spans:
            tag_a = item.find('a')
            if tag_a:
                stuff.append((tag_a.text, tag_a.get('href')))
    else:
        select_list = soup.select('p a[href]')
        for i in select_list:
            stuff.append((i.text, i.get('href')))

    return stuff

def get_stuff2(url):
    site = urlopen(url)
    soup = bs(site, 'html.parser')

    select_list = soup.select('.visit_link ul li a[href]')
    stuff = list()
    for i in select_list:
        stuff.append((i.text, i.get('href')))
    return stuff

def parse_physics(url):
    struct_link = get_link_from_button(url, 'Структура')
    cathedras = get_cathedras(struct_link)

    res = {}
    for name, url in cathedras:
        url1 = get_link_from_button(url, 'Сотрудники')
        url2 = get_link_from_button(url, 'Сотрудники кафедры')
        url3 = get_link_from_button(url, 'Коллектив кафедры')
        if url1:
            res[name] = url1
        elif url2:
            res[name] = url2
        elif url3:
            res[name] =url3

    for name, stuff_url in res.items():
        if name == 'Кафедра радиоастрономии':
            res[name] = len(get_stuff2(stuff_url))
        else:
            try:
                res[name] = len(get_stuff(stuff_url))
            except :
                res[name] = len(get_stuff2(stuff_url))
    return res

# print(parse_physics(url_phys))