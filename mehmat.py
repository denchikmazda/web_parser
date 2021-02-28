from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from ivmiit import get_link_from_button

def get_name_links_cathedras(url):
    site = urlopen(url)
    soup = bs(site,'html.parser')

    uls = soup.find_all('ul',class_='menu_list')
    cathedras = list()

    list_items = list()
    for ul in uls:
        lis = ul.find_all('li',class_='li_spec')
        for li in lis:
            list_items.append(li)

    for item in list_items:
        tag_a = item.find('a')
        if tag_a:
            if tag_a.text.startswith('Кафедpа') or tag_a.text.startswith('Кафедра'):
                cathedras.append((tag_a.text,tag_a.get('href')))
    return cathedras

def get_stuff(url):
    site = urlopen(url)
    soup = bs(site, 'html.parser')

    stuff = list()
    iframe = soup.find('iframe')
    if iframe:
        source = iframe.get('src')

        site = urlopen(source)
        soup = bs(site,'html.parser')

        spans = soup.find_all('span',class_='fio')
        for item in spans:
            tag_a = item.find('a')
            if tag_a:
                stuff.append((tag_a.text,tag_a.get('href')))
    else:
        tbody = soup.find_all('tbody')[0]
        trs = tbody.find_all('tr')
        for tr in trs:
            td = tr.find('td')
            p = td.find('p')
            a = p.find_all('a')[0]
            if a:
                stuff.append((a.text, a.get('href')))
    return stuff

def parse_mehmat(url):
    struct_link = get_link_from_button(url,'Структура')
    cathedras = get_name_links_cathedras(struct_link)

    res = {}
    for name, url in cathedras:
        url1 = get_link_from_button(url, 'Сотрудники')
        url2 = get_link_from_button(url,'Состав кафедры')
        if url1:
            res[name] = url1
        elif url2:
            res[name] = url2

    for name, stuff_url in res.items():
        res[name] = len(get_stuff(stuff_url))
    return res

print(parse_mehmat('https://kpfu.ru/math'))

