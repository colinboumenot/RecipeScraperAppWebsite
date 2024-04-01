from recipe import Recipe
import pickle
import inflect 
import re
import random

recipes = []

with open('ScrapedRecipes/all_recipes.pickle', 'rb') as f:
    recipes.extend(pickle.load(f))
with open('ScrapedRecipes/all_recipes_2.pickle', 'rb') as f:
    recipes.extend(pickle.load(f))
with open('ScrapedRecipes/all_recipes_3.pickle', 'rb') as f:
    recipes.extend(pickle.load(f))

temp_recipes = recipes
recipes = []

for item in temp_recipes:
    if item is not None:
        recipes.append(item)

measurements = set(x.strip().lower() for x in open('raw_data/foodnetwork_measurements.txt', 'r+').readlines())


## Convert all plural nouns to singular, reduces ingredients that need to be entered into food names
def plural_to_singular(ingredients):
    p = inflect.engine()
    new_ingredients = []
    for ingredient in ingredients:
        ## Certain characters that need to get filtered out from ingredient
        ingredient = ingredient.strip().replace(',', '').replace('*', '').replace('\xa0', ' ').replace(';', '').replace('"', '').replace('/', ' ').replace('.', '').replace('-', ' ').replace('(', '').replace(')', '')
        ## Handle parentheses later
        singular_phrase = []
        for word in ingredient.split(' '):
            word = word.strip()
            if word != '' and word != 'tbs':
                singular = p.singular_noun(word)
            else:
                singular = False

            if singular is not False:
                singular_phrase.append(singular)
            else:
                singular_phrase.append(word)
        new_ingredients.append(" ".join(singular_phrase).lower())
    return new_ingredients

def get_measurements(ingredient):
    matches = []
    for word in ingredient.split(' '):
        if word in measurements:
            matches.append(word)
        ## Below code was used to write errors for edgecases to a seperate file
    if len(matches) > 1:
        with open('raw_data/unknown_ingredients.txt', 'a') as f:
            f.write(ingredient + ' ' + " ".join(matches) + '\n')
            ##if len(temp) == 1 and ('and' in ingredient or 'or' in ingredient):
                ##with open('raw_data/unknown_ingredients.txt', 'a') as f:
                    ##f.write('and or ingredient ' + ingredient + ' ' + ' '.join(temp) + '\n')
            ## if (len(temp) > 1):
                ## if 'or' in ingredient.split(' '):
                    ## continue
                ##elif 'and' in ingredient.split(' '):
                    ##continue
                ## elif 'such as' in ingredient or 'recipe follow' in ingredient or 'optional' in ingredient:
                    ## continue
                ## else:
                    ## multiple_ingredient_error(ingredient, temp)
                        ##with open('raw_data/unknown_ingredients.txt', 'a') as f:
                            ## f.write('multiple ingredient ' + ingredient + ' ' + ' '.join(temp) + '\n')

    return matches

cleaned_recipes = []

for x in range(1000):
    recipe = recipes[x]
    singular_ingredients = plural_to_singular(recipe.ingredients)
    for ingredient in singular_ingredients:
        get_measurements(ingredient)

