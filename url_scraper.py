import requests
import time
import random
from bs4 import BeautifulSoup


base_url = "https://www.foodnetwork.com/recipes/recipes-a-z/"

# All categories of alphabetical recipes from the base url
url_extensions = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'xyz', '123']


# Finds length of a given page, to ensure that all recipes are scraped for each category
def page_search_length(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    lengths = soup.findAll('li', {"class": "o-Pagination__a-ListItem"})
    
    # If had to stop in process of scraping, resume from most recently printed extension
    print(url)
    return int(lengths[-2].find('a').get_text())

# Gets all recipe urls from each page of each category, and then writes them into the text file
def subpage_search(url, pages):

    # Write urls to text file for later
    text_urls = open('recipe_urls.txt', 'a')
    url_list = []

    for x in range(1, pages + 1):
        search_url = url + str(x)
        r = requests.get(search_url)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
    
            boxes = soup.findAll('ul', {"class": "m-PromoList o-Capsule__m-PromoList"})
        
            for box in boxes:
                box_urls = [urls['href'] for urls in box.find_all('a', href = True)]
                for x in box_urls:
                    url_list.append(x + '\n')

            # To avoid getting blocked
            time.sleep(random.randint(1, 2))
    
    text_urls.writelines(url_list)
    text_urls.close()

for extension in url_extensions:
    url_one = base_url + extension
    url_two = base_url + extension + '/p/'

    subpage_search(url_two, page_search_length(url_one))



    

#subpage_search(base_url + '123/p/', page_search_length(base_url + '123'))