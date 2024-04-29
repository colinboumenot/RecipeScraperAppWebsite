import pickle
import recipe

with open('cleaned_recipe_objects_standardized.pickle', 'rb') as f:
    list_x = pickle.load(f)

print(list_x)