from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


def get_link_from_button(url,button_name):
    site = urlopen(url)
    soup = bs(site, 'html.parser')

    ul = soup.find('ul',class_='menu_list_left')
    list_items = ul.find_all('li')

    for item in list_items:
        tag_a = item.find('a')
        if tag_a.text == button_name:
            return tag_a.get('href')

def get_name_link_of_cathedras_ivmiit(url):
    site = urlopen(url)
    soup = bs(site,'html.parser')

    div = soup.find('div',class_='visit_link')
    uls = div.find_all('ul')

    list_items = list()
    for ul in uls:
        list_items += ul.find_all('li',class_='li_spec')

    cathedras = list()
    for item in list_items:
        tag_a = item.find('a')
        if tag_a.text.startswith('Кафедра'):
            cathedras.append((tag_a.text, tag_a.get('href')))
    return cathedras

def get_name_link_of_teachers(url):
    site = urlopen(url)
    soup = bs(site,'html.parser')

    iframe = soup.find('iframe')
    src = iframe.get('src')

    sourse = urlopen(src)
    soup = bs(sourse, 'html.parser')

    stuff = []
    spans = soup.find_all('span', class_='fio')
    for item in spans:
        tag_a = item.find('a')
        if tag_a:
            stuff.append((tag_a.text, tag_a.get('href')))

    return stuff


def parse_ivmiit(url):
    info_button_url = get_link_from_button(url,'Об институте')
    cathedras = get_name_link_of_cathedras_ivmiit(info_button_url)

    res = {}

    for name, url in cathedras:
        stuff_url = get_link_from_button(url,'Сотрудники')
        res[name] = stuff_url

    for name, url in res.items():
        res[name] = len(get_name_link_of_teachers(url))

    return res

# print(parse_ivmiit('https://kpfu.ru/computing-technology'))

