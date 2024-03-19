from recipe import Recipe
import pickle

with open('ScrapedRecipes/all_recipes.pickle', 'rb') as f:
    recipes = pickle.load(f)

foods = set(x.strip() for x in open('raw_data/backend_food_names.txt', 'r+').readlines())

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
                    print(f"1 - {half_one} 2 - {half_two}")
                    with open('raw_data/unknown_ingredients.txt', 'a') as f:
                        f.write(' '.join(ingredient) + '\n')
                    x += 1

print(x)