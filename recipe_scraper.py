import recipe
import requests
import time
import random
from bs4 import BeautifulSoup

url = "https://www.foodnetwork.com/recipes/a-bologna-calamari-scallops-and-clams-with-roasted-fingerlings-and-arugula-salad-recipe-2040576"

def scrape_url(url):
    r = requests.get(url)

    if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            title = get_title(soup)
            time = get_time(soup)
            yield_amount = get_servings(soup)
            print(yield_amount)
    else:
          return

def get_title(soup):
    try:
        title = soup.find('span', {"class": "o-AssetTitle__a-HeadlineText"}).get_text()
    except:
         title = ""
    return title

def get_time(soup):
    try:
        total = soup.find('span', {"class": "o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total"}).get_text()
    except:
         total = ""
    return total

def get_servings(soup):
    try:
        box = soup.find('ul', {"class": "o-RecipeInfo__m-Yield"})
        yield_amount = box.find('span', {"class": "o-RecipeInfo__a-Description"}).get_text()
    except:
        yield_amount = ""
    return yield_amount
    
    
    

scrape_url(url)
    
    


    