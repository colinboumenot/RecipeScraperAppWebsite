import pickle
import recipe
from collections import defaultdict


with open('raw_data/pickle_files/ingredient_to_recipes_dict.pickle', 'rb') as f:
    ingredient_to_recipes = pickle.load(f)

with open('raw_data/pickle_files/recipe_toingredients_toquantities.pickle', 'rb') as f:
    recipes_to_quantities = pickle.load(f)

user_ingredients = dict()

for ingredient in ingredient_to_recipes:
    user_ingredients[ingredient] = [0, 0, 0, 0]

user_ingredients['salt'][0] = 99999
user_ingredients['corn'][3] = 4
user_ingredients['thyme'][3] = 8
user_ingredients['onion'][3] = 1
user_ingredients['garlic'][3] = 4
user_ingredients['bay leaf'][3] = 3
## user_ingredients['black peppercorn'][1] = 1
user_ingredients['olive oil'][0] = 1

def check_recipe_validity(recipe):
    for key in recipes_to_quantities[recipe.id]:
        totals = recipes_to_quantities[recipe.id][key]
        ## Occurs if recipe does not specify quantity for an ingredient, for this arbitrary measure we assume any amount the user has is sufficient, provided they have an ammount
        if totals == [0, 0, 0, 0]:
            if user_ingredients[key] == [0, 0, 0, 0]:
                return False
        ## Check if the user has a sufficient amount of the provided ingredient
        for x in range(4):
            if user_ingredients[key][x] < totals[x]:
                return False
    return True

def check_recipe_validity_exclusive(recipe, ingredients):
    for key in ingredients:
        totals = recipes_to_quantities[recipe.id][key]
        ## Occurs if recipe does not specify quantity for an ingredient, for this arbitrary measure we assume any amount the user has is sufficient, provided they have an ammount
        if totals == [0, 0, 0, 0]:
            if user_ingredients[key] == [0, 0, 0, 0]:
                return False
        ## Check if the user has a sufficient amount of the provided ingredient
        for x in range(4):
            if user_ingredients[key][x] < totals[x]:
                return False
    return True

## Provide user with list of recipes using all selected ingredients
def find_recipes_no_quantities(ingredients):
    return set.intersection(*(ingredient_to_recipes[x] for x in ingredients))

## Provide user with list of recipes using selected ingredients taking into account quantities, checks if you have enough of ALL ingredients in recipe
def find_recipes_quantities(ingredients):
    initial_set = find_recipes_no_quantities(ingredients)
    final_set = set()
    for recipe in initial_set:
        if check_recipe_validity(recipe):
            final_set.add(recipe)
    return final_set

## Similar to find_recipes_quantities, however this function only considers if you have enough of your preselected ingredients for the recipe
def find_recipes_quantities_exclusive(ingredients):
    initial_set = find_recipes_no_quantities(ingredients)
    final_set = set()
    for recipe in initial_set:
        if check_recipe_validity_exclusive(recipe, ingredients):
            final_set.add(recipe)
    return final_set
