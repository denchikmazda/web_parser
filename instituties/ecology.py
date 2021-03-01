from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from instituties.ivmiit import get_link_from_button

def get_name_link_of_cathedras_ecology(url):
    site = urlopen(url)
    soup = bs(site,'html.parser')

    div = soup.find('div',class_='visit_link')
    links = div.find_all('a')
    cathedras = list()
    for item in links:
        if  item.text.startswith('Кафедра'):
            cathedras.append((item.text, item.get('href')))
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


def parse_ecology(url):
    info_button_url = get_link_from_button(url, 'Структура')
    cathedras = get_name_link_of_cathedras_ecology(info_button_url)

    res = {}

    for name, url in cathedras:
        stuff_url = get_link_from_button(url, 'Состав')
        res[name] = stuff_url

    for name, url in res.items():
        res[name] = len(get_name_link_of_teachers(url))

    return res

# print(parse_ecology('https://kpfu.ru/ecology'))