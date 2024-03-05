import recipe
import requests
import time
import random
from bs4 import BeautifulSoup

url = "https://www.foodnetwork.com/recipes/trisha-yearwood/un-fried-chicken-2282177"
def scrape_url(url):
    r = requests.get(url)

    if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')

            title = get_title(soup)
            time = get_time(soup)
            yield_amount = get_servings(soup)
            level = get_level(soup)
            ingredients = get_ingredients(soup)
            steps = get_steps(soup)
            tags = get_tags(soup)

    else:
          return


## Series of Helper Methods to scrape individual components of the webpage

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

def get_level(soup):
    try:
        box = soup.find('ul', {"class": "o-RecipeInfo__m-Level"})
        level = box.find('span', {"class": "o-RecipeInfo__a-Description"}).get_text()
    except:
        level = ""
    return level

def get_ingredients(soup):
    try:
        box = soup.find('div', {"class": "o-Ingredients__m-Body"})
        ingredients_boxes = box.find_all('p', {"class": "o-Ingredients__a-Ingredient"})
        ingredients = []
        for x in ingredients_boxes:
            ingredients.append(x.find('span', {"class": "o-Ingredients__a-Ingredient--CheckboxLabel"}).get_text())
    except:
        ingredients = []
    
    ## Chops off the 'Deselect All' entry
    return ingredients[1:]

def get_steps(soup):
    try:
        box = soup.find('div', {"class": "o-Method__m-Body"})
        steps_boxes = box.find_all('li', {"class": "o-Method__m-Step"})
        steps = []
        for x in steps_boxes:
            steps.append(x.get_text())
    except:
        steps = []
    return steps

def get_tags(soup):
    try:
        box = soup.find('div', {"class": "o-Capsule__m-TagList m-TagList"})
        tag_boxes = box.find_all('a', {"class": "o-Capsule__a-Tag a-Tag"})
        tags = []
        for x in tag_boxes:
            tags.append(x.get_text())
    except:
        tags = []
    return tags

    
    


    