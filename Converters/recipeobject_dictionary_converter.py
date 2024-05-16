import pickle
import recipe
from collections import defaultdict

with open('raw_data/pickle_files/cleaned_recipe_objects_standardized.pickle', 'rb') as f:
    recipes = pickle.load(f)



recipes_to_dictionary = defaultdict()


## Remaking recipes as a dictionary, the keys are the ingredients, and the values is a table showing the amount of grams, cups, packages, wholes needed for that recipe
def recipe_as_dictionary(recipe):
    recipe_dictionary = dict()
    for ingredient in recipe.ingredients_backend_side:
        if len(ingredient.split('@')) > 1:
            measurement, ingredient = ingredient.split('@')
            quantity, unit = measurement.split(' ')
            quantity = float(quantity)
            if ingredient not in recipe_dictionary:
                recipe_dictionary[ingredient] = [0, 0, 0, 0]
            
            if unit == 'gram':
                recipe_dictionary[ingredient][0] += quantity
            elif unit == 'cup':
                recipe_dictionary[ingredient][1] += quantity
            elif unit == 'package':
                recipe_dictionary[ingredient][2] += quantity
            else:
                recipe_dictionary[ingredient][3] += quantity

        else:
            if ingredient not in recipe_dictionary:
                recipe_dictionary[ingredient] = [0, 0, 0, 0]

    return recipe_dictionary

for x in recipes:
    ## Weird glitch with this recipe, fix later if time
    recipe_dictionary = recipe_as_dictionary(x)
    hash_add = 0
    if x.steps:
        hash_add = len(x.steps[0])

    recipes_to_dictionary[x.id] = recipe_dictionary

with open('raw_data/pickle_files/recipe_toingredients_toquantities.pickle', 'wb') as f:
    pickle.dump(recipes_to_dictionary, f)