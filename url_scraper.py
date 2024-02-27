import requests
from bs4 import BeautifulSoup

base_url = "https://www.foodnetwork.com/recipes/recipes-a-z/"

url_extensions = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'xyz', '123']


def page_search_length(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    max_pages = 0

    lengths = soup.findAll('li', {"class": "o-Pagination__a-ListItem"})
    print(lengths[-2].find('a').get_text())

def subpage_search(url, pages):
    for x in range(1, pages + 1):
        search_url = url + x
        r = requests.get(url)

page_search_length(base_url + 'b')
