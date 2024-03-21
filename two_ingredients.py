from recipe import Recipe
import pickle
import inflect 

with open('ScrapedRecipes/all_recipes.pickle', 'rb') as f:
    recipes = pickle.load(f)

foods = set(x.strip() for x in open('raw_data/backend_food_names.txt', 'r+').readlines())
recipe = recipes[0]

## Converting plural to singular to avoid having to enter same ingredients multiple times
p = inflect.engine()
new_ingredients = []
for x in recipe.ingredients:
    x = x.replace(',', '')
    singular_phrase = []
    for y in x.split(' '):
        singular = p.singular_noun(y)
        if singular is not False:
            singular_phrase.append(singular)
        else:
            singular_phrase.append(y)
    new_ingredients.append(" ".join(singular_phrase).lower())
recipe.ingredients = new_ingredients

print(recipe.ingredients)

matches = []
for ingredient in recipe.ingredients:
    temp = []
    for food in foods:
        if food in ingredient and len(set(food.split(' ')).intersection(set(ingredient.split(' ')))) == len(food.split(' ')):
                duplicate = False
                for x in temp:
                    if food in x:
                        duplicate = True
                    if x in food:
                        temp.remove(x)
                if not duplicate:
                    temp.append(food)
    for x in temp:
        matches.append(x)

    
print(matches)

x = 0

for recipe in recipes:
    if recipe is not None:
        for ingredient in recipe.ingredients:
            ingredient = ingredient.split(',')[0]
            if 'and' in ingredient.split(' '):
                ingredient = ingredient.split(' ')
                half_one = ' '.join(ingredient[:ingredient.index('and')]).lower()
                half_two = ' '.join(ingredient[ingredient.index('and') + 1:]).lower()
                ## print(f"1 - {ingredient.split('and')[0]} 2 - {ingredient.split('and')[1]}")
                matches = []
                for food in foods:
                    if food in half_one:
                        matches.append(food)
                    if food in half_two:
                        matches.append(food)
                if len(matches) == 0:
                    ## print(f"1 - {half_one} 2 - {half_two}")
                    with open('raw_data/unknown_ingredients.txt', 'a') as f:
                        f.write(' '.join(ingredient) + '\n')
                    x += 1

print(x)

