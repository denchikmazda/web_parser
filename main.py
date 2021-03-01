from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import config

def get_name_link_of_institutes(url):
    site = urlopen(url)
    soup = bs(site, 'html.parser')

    ul = soup.find_all('ul', class_='menu_list')[:2]
    lis = ul[0].find_all('li', class_='li_spec')
    lis += ul[1].find_all('li', class_='li_spec')

    institutes = [(li.find('a').text, li.find('a').get('href')) for li in lis]

    return institutes


if __name__ == '__main__':
    print('h1')
