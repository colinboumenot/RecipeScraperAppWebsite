import pickle
import recipe
from collections import defaultdict


with open('raw_data/pickle_files/ingredient_to_recipes_dict.pickle', 'rb') as f:
    ingredient_to_recipes = pickle.load(f)

with open('raw_data/pickle_files/recipe_toingredients_toquantities.pickle', 'rb') as f:
    recipes_to_quantities = pickle.load(f)

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

def check_recipe_validity_no_quantity(recipe):
    for key in recipes_to_quantities[recipe.id]:
        if user_ingredients[key] == [0, 0, 0, 0]:
            return False
    return True

## Provide user with list of recipes using all selected ingredients, checking all ingredients in recipe
def find_recipes_no_quantities(ingredients):
    intial_recipes = set.intersection(*(ingredient_to_recipes[x] for x in ingredients))
    final_recipes = set()
    for recipe in intial_recipes:
        if check_recipe_validity_no_quantity:
            final_recipes.add(recipe)
    return final_recipes

## Provide user with list of recipes using all selected ingredients, checking only entered ingredients
def find_recipes_no_quantities_exclusive(ingredients):
    return set.intersection(*(ingredient_to_recipes[x] for x in ingredients))

## Provide user with list of recipes using selected ingredients taking into account quantities, checks if you have enough of ALL ingredients in recipe
def find_recipes_quantities(ingredients):
    initial_set = find_recipes_no_quantities_exclusive(ingredients)
    final_set = set()
    for recipe in initial_set:
        if check_recipe_validity(recipe):
            final_set.add(recipe)
    return final_set

## Similar to find_recipes_quantities, however this function only considers if you have enough of your preselected ingredients for the recipe
def find_recipes_quantities_exclusive(ingredients):
    initial_set = find_recipes_no_quantities_exclusive(ingredients)
    final_set = set()
    for recipe in initial_set:
        if check_recipe_validity_exclusive(recipe, ingredients):
            final_set.add(recipe)
    return final_set
