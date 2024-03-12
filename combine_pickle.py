import pickle
from recipe import Recipe

## This file checks contents of pickle file after running recipe_scraper use with test.txt

with open('PickledData/recipe_data.pickle', 'rb') as f:
    test_list = pickle.load(f)

with open('PickledData/recipe_data.pickle', 'rb') as f:
    test_list = pickle.load(f)


for x in test_list:
    if x is not None:
        print(x.title)