from measurement_converter import units_to_master_measurement

quantified_units = {'gill', 'ounce', 'kilogram', 'gallon', 'liter', 'milliliter', 'quart', 'teaspoon', 'pint', 'tablespoon', 'pound', 'can', 'bag', 'jar', 'bottle', 'container', 'tube'}


## TODO user_ingredients is the dictionary of the user provided ingredients, this will need to be updated once that is implemented

## Provide input in format ingredient%quantity%unit, quantity should be negative if user is removing ingredient
def input_cleanup(user_input):
    if len(user_input.split('%')) > 1:
        ingredient, quantity, unit = user_input.split('%')
        quantity = float(quantity)
        if quantity in quantified_units:
            quantity, unit = units_to_master_measurement(quantity, unit)

        update_ingredients_quantity(ingredient, quantity, unit)
    else:
        ingredient = user_input
        update_ingredients_no_quantity(ingredient)

def update_ingredients_quantity(ingredient, quantity, unit):
    if quantity == 'gram':
        user_ingredients[ingredient][0] += quantity
    elif quantity == 'cup':
        user_ingredients[ingredient][1] += quantity
    elif quantity == 'package':
        user_ingredients[ingredient][2] += quantity
    else:
        user_ingredients[ingredient][3] += quantity

## If user chooses no quantity, we assume they have an infinite amount of the ingredient
def update_ingredients_quantity(ingredient):
    user_ingredients[quantity] = [99999, 99999, 99999, 99999]