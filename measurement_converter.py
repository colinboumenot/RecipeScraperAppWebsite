import pickle
from recipe import Recipe
from collections import defaultdict

recipes = []

with open('cleaned_recipe_objects.pickle', 'rb') as f:
    recipes = pickle.load(f)

## Converting all common measurements to ounces
volume_ingredients = set()
mass_ingredients = set()

def units_to_ounce(quantity, unit, ingredient):
    if unit == 'pound':
        quantity *= 16
        mass_ingredients.add(ingredient)
        return quantity, 'ounce'
    elif unit == 'gram':
        quantity /= 28.35
        mass_ingredients.add(ingredient)
        return quantity, 'ounce'
    elif unit == 'kilogram':
        quantity *= 35.274
        mass_ingredients.add(ingredient)
        return quantity, 'ounce'
    elif unit == 'gill':
        quantity *= 4
        volume_ingredients.add(ingredient)
        return quantity, 'fl ounce'
    elif unit == 'gallon':
        quantity *= 128
        volume_ingredients.add(ingredient)
        return quantity, 'fl ounce'
    elif unit == 'liter':
        quantity *= 33.814
        volume_ingredients.add(ingredient)
        return quantity, 'fl ounce'
    elif unit == 'milliliter':
        quantity /= 29.574
        volume_ingredients.add(ingredient)
        return quantity, 'fl ounce'
    elif unit == 'quart':
        quantity *= 32
        volume_ingredients.add(ingredient)
        return quantity, 'fl ounce'
    elif unit == 'pint':
        quantity *= 16
        volume_ingredients.add(ingredient)
        return quantity, 'fl ounce'
    elif unit == 'cup':
        quantity *= 8
        volume_ingredients.add(ingredient)
        return quantity, 'fl ounce'
    elif unit == 'tablespoon':
        quantity /= 2
        volume_ingredients.add(ingredient)
        return quantity, 'fl ounce'
    elif unit == 'teaspoon':
        quantity /= 6
        volume_ingredients.add(ingredient)
        return quantity, 'fl ounce'
    else:
        ## Should not occur, check unit for error
        print(unit)
    

abbreviation_conversion = {
    'lb' : 'pound',
    'tsp' : 'teaspoon',
    'tbsp' : 'tablespoon',
    'tbs' : 'tablespoon', 
    'g' : 'gram',
    'ml' : 'milliliter',
    'kg' : 'kilogram',
    'pt' : 'pint',
    'qt' : 'quart',
    'l' : 'liter',
    'litre' : 'liter',
    'tbl' : 'tablespoon',
    'oz' : 'ounce',
    'cc' : 'milliliter',
}

shorthanded_measurements = set()
for key in abbreviation_conversion:
    shorthanded_measurements.add(key)

counter = defaultdict(int)
quantified_units = {'gill', 'kilogram', 'gallon', 'liter', 'milliliter', 'gram', 'quart', 'teaspoon', 'cup', 'pint', 'tablespoon', 'pound'}
cleaned_recipes = []
mass_units = {'pound', 'gram', 'kilogram', 'ounce'}

for recipe in recipes:
    recipe_dict = defaultdict(set)
    for ingredient in recipe.ingredients_backend_side:
        if len(ingredient.split('@')) > 1:
            measurement = ingredient.split('@')[0]
            ingredient = ingredient.split('@')[1]
            quantity, unit = measurement.split(' ')
            if unit in shorthanded_measurements:
                unit = abbreviation_conversion[unit]




print(len(volume_ingredients & mass_ingredients))