from recipe import Recipe
import pickle
import inflect 
import re

with open('ScrapedRecipes/all_recipes.pickle', 'rb') as f:
    recipes = pickle.load(f)

temp_recipes = recipes
recipes = []
new_ingredients = set()

for item in temp_recipes:
    if item is not None:
        recipes.append(item)

foods = set(x.strip().lower() for x in open('raw_data/backend_food_names.txt', 'r+').readlines())

## Words that look plural but are really singular, brute force approach but still works
edge_cases = ['watercress', 'delicious', 'cress', 'peppercress', 'guinness', 'bass', 'christmas', 'grits', 'lotus', 'seabass', 'angus', 'cablres', 'ras', 'hummus', 'fries', 'skinless', "'s", 'octopus', 'pastis', 'hibiscus', 'molasses', 'lemongrass', 'couscous', 'cactus', 'citrus', 'bitters', 'swiss', 'gras', 'wheatgrass', 'moss', 'jus', 'as']

## Convert all plural nouns to singular, reduces ingredients that need to be entered into food names
def plural_to_singular(ingredients):
    p = inflect.engine()
    new_ingredients = []
    for ingredient in ingredients:
        ingredient = ingredient.strip().replace(',', '').replace('*', '').replace('\xa0', ' ').replace(';', '').replace('"', '').replace('/', ' ').replace('.', '').replace('®', '').replace('è', 'e')
        ## Handle parentheses later
        singular_phrase = []
        for word in ingredient.split(' '):
            word = word.strip()
            if word not in edge_cases and "'s" not in word and word != '':
                    singular = p.singular_noun(word)
            else:
                singular = False

            if singular is not False:
                singular_phrase.append(singular)
            else:
                singular_phrase.append(word)
        new_ingredients.append(" ".join(singular_phrase).lower())
    return new_ingredients

## Takes string that has more ingredients than it should, and finds the individual ingredients oftentimes these ingredients are compounds
## Ex "pork shoulder" should be 1 ingredient, before this function 'pork' and 'shoulder' were two seperate ingredients
def build_new_ingredient(ingredient, matches, start):
    new_ingredient = ''
    found_items = []

    for x in range(start, len(ingredient)):
        if ingredient[x] in matches:
            new_ingredient += ingredient[x] + ' '
            found_items.append(ingredient[x])
        else:
            break
    
    for x in found_items:
        if x in matches:
            matches.remove(x)
    
    if len(matches) > 0:
        new_start = min(ingredient.index(word) for word in matches)
        return new_start, matches, new_ingredient.strip()
    else:
        return -1, matches, new_ingredient.strip()


## Called if too many ingredients detected
def multiple_ingredient_error(ingredient, matches):
    ## print(f"{ingredient} matches: {matches}")
    ingredient = ingredient.split(' ')
    ingredients = []
    edited_matches = []
    for x in matches:
        x = x.split(' ')
        for word in x:
            edited_matches.append(word)
    start = min(ingredient.index(word) for word in edited_matches)
    
    while len(edited_matches) > 0:
        start, edited_matches, new_ingredient = build_new_ingredient(ingredient, edited_matches, start)
        if new_ingredient != '':
            ingredients.append(new_ingredient)
            if new_ingredient not in foods:
                new_ingredients.add(new_ingredient)

    ## print(ingredients)


def get_ingredients(recipe):
    matches = []
    for ingredient in recipe.ingredients:
        ## Get rid of contents inside parentheses, useful for determining units later on, but not for ingredients
        ingredient = re.sub("[\(\[].*?[\)\]]", "", ingredient)
        temp = []
        duplicates = []
        for food in foods:
            ## Check first if food substring appears in ingredients, then check if words of substring appear in ingredient string as set
            if food in ingredient and (len(set(food.split(' ')).intersection(set(ingredient.split(' ')))) == len(food.split(' '))):
                    duplicate = False
                    for previous in temp:
                        if food in previous:
                            duplicate = True
                        if previous in food:
                            duplicates.append(previous)
                    if not duplicate:
                        temp.append(food)
            ## Above method works for all ingredients besides half and half so far, since half and half as a set is only (half, and)
            elif food in ingredient and food == 'half and half':
                    duplicate = False
                    for previous in temp:
                        if food in previous:
                            duplicate = True
                        if previous in food:
                            duplicates.append(previous)
                    if not duplicate:
                        temp.append(food)

        for item in duplicates:
            if item in temp:
                temp.remove(item)
        
        ## Edge case with garlic
        
        if 'garlic' in temp:
            if 'clove' in temp:
                temp.remove('clove')
            if 'cloves' in temp:
                temp.remove('cloves')

        ## if len(temp) == 0:
            ## if 'water' in set(ingredient.split(' ')) or 'ice' in set(ingredient.split(' ')) or 'cooking spray' in ingredient:
                ## continue
            ## elif 'recipe follow' in ingredient:
                ## continue
            ## else:
                ## with open('raw_data/unknown_ingredients.txt', 'a') as f:
                    ## f.write('no ingredient ' + ingredient + '\n')
                ## pass
        ##if len(temp) == 1 and ('and' in ingredient or 'or' in ingredient):
            ##with open('raw_data/unknown_ingredients.txt', 'a') as f:
                ##f.write('and or ingredient ' + ingredient + ' ' + ' '.join(temp) + '\n')
        if (len(temp) > 1):
            if 'or' in ingredient.split(' '):
                continue
            elif 'and' in ingredient.split(' '):
                continue
            elif 'such as' in ingredient or 'recipe follow' in ingredient or 'optional' in ingredient:
                continue
            else:
                multiple_ingredient_error(ingredient, temp)
                with open('raw_data/unknown_ingredients.txt', 'a') as f:
                    f.write('multiple ingredient ' + ingredient + ' ' + ' '.join(temp) + '\n')
        for x in temp:
            matches.append(x)
    return matches

# recipe.ingredients = plural_to_singular(recipe.ingredients)
# print(get_ingredients(recipe))

print(len(recipes))

for x in range(20000, len(recipes)):
    recipe = recipes[x]
    recipe.ingredients = plural_to_singular(recipe.ingredients)
    get_ingredients(recipe)

## Helper method to sort ingredient file alphabetically
## def sort_file(input_file, output_file):
    ## with open(input_file) as f:
        ## with open(output_file, "w") as o:
            ## o.write("\n".join(sorted(f.read().splitlines())))

## sort_file("raw_data/backend_food_names.txt", "raw_data/food_names.txt")

with open('raw_data/new_ingredients.txt', 'w+') as f:
    for x in new_ingredients:
        f.write(x + '\n')
