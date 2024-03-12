from recipe import Recipe
import requests
import pickle
from time import time, sleep
import random
from bs4 import BeautifulSoup


with open('recipe_data.pickle', 'rb') as f:
    try:
        recipe_list = pickle.load(f)
    except:
        recipe_list = []
    f.close()

with open('recipe_data.pickle', 'wb') as f:
    pickle.dump(recipe_list, f)
    f.close()

## Attempt to speed up request time by reusing connection
session = requests.Session()

## Extension to add in front of scraped urls
url_extension = "https:"

def scrape_url(url):

    start_time = time()

    url = url_extension + url
    url = url.strip()
    session = requests.get(url)

    ## Time for completing request
    print(f"Fetch {(time() - start_time)}")

    if session.status_code == 200:
            soup = BeautifulSoup(session.text, 'lxml')

            title = get_title(soup)
            timeing = get_time(soup)
            yield_amount = get_servings(soup)
            level = get_level(soup)
            ingredients = get_ingredients(soup)

            ## TODO clean up steps further
            steps = get_steps(soup)
            tags = get_tags(soup)

            recipe = Recipe(title, timeing, yield_amount, level, ingredients, steps, tags)

            ## Timing for scraping website
            ##print(f"Scrape {(time() - start_time)}")

            return recipe

    else:
          return None


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


## Limiting to 5 requests per second at most, to avoid getting blocked, change depending on future results

## counter = 0
for line in open('recipe_urls.txt', 'r'):

    ## Not most efficient way, but helps slow down time between requests
    time_one = time()
    finished_list = open('finished_urls.txt', 'a+')
    finished_list.seek(0)
    contents = finished_list.read()
    time_two = time() - time_one

    if line not in contents:

        ## counter += 1
        recipe = scrape_url(line)

        time_three = time()
        with open('recipe_data.pickle', 'rb') as f:
            recipe_list = pickle.load(f)
        
        if recipe is not None:
            recipe_list.append(recipe)

        with open('recipe_data.pickle', 'wb') as f:
            pickle.dump(recipe_list, f)
            finished_list.writelines(line)
            finished_list.close()

        ## if counter == 5:
            ## counter = 0
            ## sleep(random.randint(1, 2))

        ## Timing for managing data after scraping
        ##print(f"Process {time() - time_three + time_two}")
    else:
        finished_list.close()
        continue
        
    ## TODO find somewhere to dump recipes