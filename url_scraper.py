import requests
import time
import random
from bs4 import BeautifulSoup



text_urls = open('recipe_urls.txt', 'w+')

base_url = "https://www.foodnetwork.com/recipes/recipes-a-z/"

url_extensions = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'xyz', '123']


def page_search_length(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    lengths = soup.findAll('li', {"class": "o-Pagination__a-ListItem"})
    

    return int(lengths[-2].find('a').get_text())

def subpage_search(url, pages):
    url_list = []

    for x in range(1, pages + 1):
        search_url = url + str(x)
        r = requests.get(search_url)
        soup = BeautifulSoup(r.text, 'lxml')
    
        boxes = soup.findAll('ul', {"class": "m-PromoList o-Capsule__m-PromoList"})
        
        for box in boxes:
            box_urls = [urls['href'] for urls in box.find_all('a', href = True)]
            for x in box_urls:
                url_list.append(x + '\n')

        time.sleep(random.randint(1, 3))
    
    text_urls.writelines(url_list)

    

#subpage_search(base_url + '123/p/', page_search_length(base_url + '123'))