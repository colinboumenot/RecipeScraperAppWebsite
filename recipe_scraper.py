from recipe import Recipe
import requests
import pickle
import time
import random
from bs4 import BeautifulSoup


recipe_list = []

with open('recipe_data.pickle', 'wb') as f:
    pickle.dump(recipe_list, f)
    f.close()

## Extension to add in front of scraped urls
url_extension = "https:"

def scrape_url(url):
    url = url_extension + url
    url = url.strip()
    r = requests.get(url)

    if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')

            title = get_title(soup)
            time = get_time(soup)
            yield_amount = get_servings(soup)
            level = get_level(soup)
            ingredients = get_ingredients(soup)

            ## TODO clean up steps further
            steps = get_steps(soup)
            tags = get_tags(soup)

            recipe = Recipe(title, time, yield_amount, level, ingredients, steps, tags)

            return recipe

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


## Limiting to 5 requests per second at most, to avoid getting blocked, change depending on future results

counter = 0
for line in open('recipe_urls.txt', 'r'):

    finished_list = open('finished_urls.txt', 'a+')
    finished_list.seek(0)
    contents = finished_list.read()

    if line not in contents:
        finished_list.writelines(line)
        finished_list.close()

        counter += 1
        recipe = scrape_url(line)

        with open('recipe_data.pickle', 'rb') as f:
            recipe_list = pickle.load(f)
            f.close()

        recipe_list.append(recipe)

        with open('recipe_data.pickle', 'wb') as f:
            pickle.dump(recipe_list, f)
            f.close()

        if counter == 5:
            counter = 0
            time.sleep(random.randint(1, 2))
    else:
        continue
        
    ## TODO find somewhere to dump recipes