import measurement_parser
import ingredient_parser
from recipe import Recipe
import pickle
import random

recipes = []


with open('ScrapedRecipes/all_recipes.pickle', 'rb') as f:
    recipes.extend(pickle.load(f))
with open('ScrapedRecipes/all_recipes_2.pickle', 'rb') as f:
    recipes.extend(pickle.load(f))
with open('ScrapedRecipes/all_recipes_3.pickle', 'rb') as f:
    recipes.extend(pickle.load(f))

temp_recipes = recipes
recipes = []

for item in temp_recipes:
    if item is not None:
        recipes.append(item)

## Foods are first pulled out, then measurements are pulled out, the two lists are compared to each other and depending on the difference in lengths a certain procedure is followed to add the itemized ingredient to the final list
def clean_ingredients(ingredients):

    if ingredients == []:
        return None
    else:
        cleaned_ingredients = []

        for ingredient in ingredients:
            food_filter = ingredient_parser.plural_to_singular(ingredient)
            foods = ingredient_parser.get_ingredients(food_filter)

            if len(foods) > 0:
                measurement_filter = measurement_parser.plural_to_singular(ingredient)
                measurements = measurement_parser.get_measurements(measurement_filter)

                if len(measurements) == len(foods):
                    for x in range(len(measurements)):
                        cleaned_ingredients.append(measurements[x] + '@' + foods[x])
                elif len(measurements) > len(foods):
                    if len(foods) == 1:
                        for measurement in measurements:
                            cleaned_ingredients.append(measurement + '@' + foods[0])
                    else:
                        ## Generally means that several ingredient options were listed with only one being required, for simplicity we just take the first one
                        if 'or' in ingredient.split(' '):
                            cleaned_ingredients.append(measurements[0] + '@' + foods[0])
                        ## Very rare case (occured 5 times in 1000 recipes tested), generally occurs when several options for ingredient listed Ex. 1/2 stick or 4 ounces of butter rare enough error that it is not a large time sink to manually fix
                        else:
                            for food in foods:
                                cleaned_ingredients.append(food)
                elif len(foods) > len(measurements):
                    if len(measurements) == 1:
                        for food in foods:
                            cleaned_ingredients.append(measurements[0] + '@' +  food)
                    elif len(measurements) == 0:
                        for food in foods:
                            cleaned_ingredients.append(food)
                            ## The majority of the time this is not a problem, usually occurs if ingredient is very simple, such as salt or pepper
                            ## with open('raw_data/unknown_ingredients.txt', 'a+') as f:
                                ## f.write('more foods ' + ingredient + '\n')
                    else:
                        if 'or' in ingredient.split(' '):
                            cleaned_ingredients.append(measurements[0] + '@' + foods[0])
                        ## Occured 1 time in 1000 recipes tested, 1 pound andouille, chorizo, or other smoked sausage cut crosswise into 1/4 inch slices rare enough error we just ignore
                        else:
                            for food in foods:
                                cleaned_ingredients.append(food)
        return cleaned_ingredients

x = -1
## Going through each recipe, if it has ingredients it is added to the pickle file for later
cleaned_recipes = []
for recipe in recipes:
    x += 1
    print(x)
    clean_recipe = clean_ingredients(recipe.ingredients)

    if clean_recipe is not None:
        new_recipe = Recipe(recipe.title, recipe.time, recipe.servings, recipe.difficulty, recipe.ingredients, recipe.steps, recipe.tags)
        new_recipe.set_ingredients_backend_side(clean_recipe)
        cleaned_recipes.append(new_recipe)

with open('cleaned_recipes.pickle', 'wb') as f:
    pickle.dump(cleaned_recipes, f)

## sample = random.sample(recipes, 200)

## for x in sample:
    ## recipe = x
    ## with open('recipe_sample.txt', 'a+') as f:
        ## f.write('old ' + " ".join(recipe.ingredients) + '\n\n' + 'new ' + " ".join(clean_ingredients(recipe.ingredients)) + '\n')