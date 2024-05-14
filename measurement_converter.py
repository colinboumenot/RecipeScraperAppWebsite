import pickle
from recipe import Recipe
from collections import defaultdict

recipes = []
food_measurements = defaultdict(set)

with open('cleaned_recipe_objects.pickle', 'rb') as f:
    recipes = pickle.load(f)

## Converting all volume measurements to cups, and all mass measurements to grams since recipes are from American site, we assume that ounces in a recipe refers to mass

def units_to_ounce(quantity, unit):
    quantity = float(quantity)
    if unit == 'pound':
        quantity *= 453.6
        return quantity, 'gram'
    elif unit == 'ounce':
        quantity *= 28.35
        return quantity, 'gram'
    elif unit == 'kilogram':
        quantity *= 1000
        return quantity, 'gram'
    elif unit == 'gill':
        quantity /= 2
        return quantity, 'cup'
    elif unit == 'gallon':
        quantity *= 16
        return quantity, 'cup'
    elif unit == 'liter':
        quantity *= 4.227
        return quantity, 'cup'
    elif unit == 'milliliter':
        quantity /= 236.6
        return quantity, 'cup'
    elif unit == 'quart':
        quantity *= 4
        return quantity, 'cup'
    elif unit == 'pint':
        quantity *= 2
        return quantity, 'cup'
    elif unit == 'tablespoon':
        quantity /= 16
        return quantity, 'cup'
    elif unit == 'teaspoon':
        quantity /= 48
        return quantity, 'cup'
    elif unit == 'can':
        quantity *= 2.5
        return quantity, 'cup'
    elif unit == 'bag':
        quantity *= 4
        return quantity, 'cup'
    elif unit == 'jar':
        quantity *= 2
        return quantity, 'cup'
    elif unit == 'bottle':
        quantity *= 3.17
        return quantity, 'cup'
    elif unit == 'container':
        quantity *= 2
        return quantity, 'cup'
    elif unit == 'tube':
        quantity *= 0.56
        return quantity, 'cup'
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
## Units that we can convert, excludes cups and grams, since they are the base conversion
quantified_units = {'gill', 'ounce', 'kilogram', 'gallon', 'liter', 'milliliter', 'quart', 'teaspoon', 'pint', 'tablespoon', 'pound', 'can', 'bag', 'jar', 'bottle', 'container', 'tube'}
cleaned_recipes = []
slices = set()

for recipe in recipes:
    new_ingredients = []
    for ingredient in recipe.ingredients_backend_side:
        if len(ingredient.split('@')) > 1:
            measurement = ingredient.split('@')[0]
            ingredient = ingredient.split('@')[1]
            quantity, unit = measurement.split(' ')
            if unit in shorthanded_measurements:
                unit = abbreviation_conversion[unit]
            ## Handles very specific edge case (8 times in all recipes) where weird ingredient is associated with 'slice' term, such as '2 slice no sugar, bacon' fix these manually due to low amount of occurences
            if unit == 'slice' and ingredient in ['salt', 'sugar', 'egg', 'lime juice', 'orange juice', 'buttermilk', 'whole milk']:
                for ingredient in input(f"{recipe.ingredients} ").split('/'):
                    unit, ingredient = ingredient.split('@')
                    quantity, unit = unit.split(' ')
                    if unit in quantified_units:
                        quantity, unit = units_to_ounce(quantity, unit)
                    new_ingredients.append(str(quantity) + ' ' + unit + '@' + ingredient)
            else:       
                if unit in quantified_units:
                    quantity, unit = units_to_ounce(quantity, unit)
                ## Creating dictionary for all units of measurement associated with an ingredient, will be used later when users input ingredients
                food_measurements[ingredient].add(unit)
                new_ingredients.append(str(quantity) + ' ' + unit + '@' + ingredient)
        else:
            new_ingredients.append(ingredient)

    recipe.set_ingredients_backend_side(new_ingredients)
    cleaned_recipes.append(recipe)

with open('cleaned_recipe_objects_standardized.pickle', 'wb') as f:
    pickle.dump(cleaned_recipes, f)
with open('food_measurements.pickle', 'wb') as f:
    pickle.dump(food_measurements, f)

