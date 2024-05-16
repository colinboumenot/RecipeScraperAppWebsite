import pickle
import recipe
from collections import defaultdict

with open('raw_data/pickle_files/cleaned_recipe_objects_standardized.pickle', 'rb') as f:
    recipes = pickle.load(f)

ingredient_to_recipes = defaultdict(set)

## Creating dictionary with ingredients as keys for recipes they are associated with

for x in recipes:
    for ingredient in x.ingredients_backend_side:
        if len(ingredient.split('@')) > 1:
            ingredient_to_recipes[ingredient.split('@')[1]].add(x)
        else:
            ingredient_to_recipes[ingredient].add(x)

with open('ingredient_to_recipes_dict.pickle', 'wb') as f:
    pickle.dump(ingredient_to_recipes, f)