import pickle
import recipe
from collections import defaultdict

with open('raw_data/pickle_files/cleaned_recipe_objects_standardized.pickle', 'rb') as f:
    recipes = pickle.load(f)

for x in recipes:
    x.set_id()

with open('raw_data/pickle_files/cleaned_recipe_objects_standardized.pickle', 'wb') as f:
    pickle.dump(recipes, f)