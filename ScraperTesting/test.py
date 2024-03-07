import pickle
from recipe import Recipe

## This file checks contents of pickle file after running recipe_scraper for test.txt

with open('recipe_data.pickle', 'rb') as f:
    test_list = pickle.load(f)

print(test_list)

