import pickle
import recipe
from collections import Counter, defaultdict

with open('raw_data/pickle_files/cleaned_recipe_objects_standardized.pickle', 'rb') as f:
    recipes = pickle.load(f)

sorted_list = []
sorted_dict = defaultdict(int)
## Frequency list for ingredients to assist with ingredient searching function

for x in recipes:
    for ingredient in x.ingredients_backend_side:
        if len(ingredient.split('@')) > 1:
            sorted_dict[(ingredient.split('@')[1])] += 1
        else:
            sorted_dict[(ingredient)] += 1

for key in sorted_dict:
    sorted_list.append(key)

sorted_list = sorted(set(sorted_list), key = lambda x :sorted_dict[(x)], reverse = True)

with open('frequency_list.txt', 'w+') as f:
    for line in sorted_list:
        f.writelines(line + '\n')