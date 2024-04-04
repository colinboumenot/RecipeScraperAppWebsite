import measurement_parser
import ingredient_parser
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

## Foods are first pulled out, then measurements are pulled out, the two lists are compared to each other and depending on the difference in lengths a certain procedure is followed to add the itemized ingredient to the final list
def clean_ingredients(ingredients):

    if ingredients == []:
        return None
    else:
        cleaned_ingredients = []

        for ingredient in ingredients:
            food_filter = ingredient_parser.plural_to_singular(ingredient)
            foods = ingredient_parser.get_ingredients(food_filter)

            if len(foods) > 0:
                measurement_filter = measurement_parser.plural_to_singular(ingredient)
                measurements = measurement_parser.get_measurements(measurement_filter)

                if len(measurements) == len(foods):
                    for x in range(len(measurements)):
                        cleaned_ingredients.append(measurements[x] + '@' + foods[x])
                elif len(measurements) > len(foods):
                    if len(foods) == 1:
                        for measurement in measurements:
                            cleaned_ingredients.append(measurement + '@' + foods[0])
                    else:
                        ## Very rare case (occured 5 times in 1000 recipes tested), generally occurs when several options for ingredient listed Ex. 1/2 stick or 4 ounces of butter rare enough error that it is faster to just manually fix
                        manual_fix = input(f"{ingredient}")
                        for x in manual_fix.split('/'):
                            clean_ingredients.append(x)
                        with open('raw_data/unknown_ingredients.txt', 'a+') as f:
                            f.write('more measurements ' + ingredient + '\n')
                elif len(foods) > len(measurements):
                    if len(measurements) == 1:
                        for food in foods:
                            cleaned_ingredients.append(measurements[0] + '@' +  food)
                    elif len(measurements) == 0:
                        for food in foods:
                            cleaned_ingredients.append(food)
                            ## The majority of the time this is not a problem, usually occurs if ingredient is very simple, such as salt or pepper
                            with open('raw_data/unknown_ingredients.txt', 'a+') as f:
                                f.write('more foods ' + ingredient + '\n')
                    else:
                        ## Occured 1 time in 1000 recipes tested, 1 pound andouille, chorizo, or other smoked sausage cut crosswise into 1/4 inch slices rare enough error that we just manually edit it
                        manual_fix = input(f"{ingredient}")
                        for x in manual_fix.split('/'):
                            clean_ingredients.append(x)
                        with open('raw_data/unknown_ingredients.txt', 'a+') as f:
                            f.write('more foods x' + ingredient + '\n')
        return cleaned_ingredients


for x in range(1000):
    recipe = recipes[x]
    clean_ingredients(recipe.ingredients)
    print(x)