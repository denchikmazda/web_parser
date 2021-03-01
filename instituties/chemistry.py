from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from instituties.ivmiit import get_link_from_button

url_chem = 'https://kpfu.ru/chemistry'

def get_cathedras(url):
    site = urlopen(url)
    soup = bs(site, 'html.parser')

    cathedras = list()
    ul = soup.find('ul',class_='menu_list')
    list_items = ul.find_all('li',class_='li_spec')
    for item in list_items:
        tag_a = item.find('a')
        if tag_a:
            if tag_a.text.startswith('Кафедра'):
                cathedras.append((tag_a.text,tag_a.get('href')))
    return cathedras

r = get_cathedras('https://kpfu.ru/chemistry/struktura')
for it in r:
    print(it)