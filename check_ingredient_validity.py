import os
import platform

#check if typed ingredient is a real ingredient
def check_ingredient(ingredient):
    all_foods = get_all_foods()
    for food in all_foods:
        if food == ingredient:
            return True
    return False

#Looks at inputed ingredient if it's not valid and finds closest match to what it should be
def get_nearest_food(ingredient:str):
    current_guess = (9999, None)
    all_foods = get_all_foods()
    for food in all_foods:
        edit_distance = check_edit_distance(ingredient, food)
        if edit_distance < current_guess[0]:
            current_guess = (edit_distance, food)
    return current_guess

def check_edit_distance(ingredient:str, food:str):
    ingredient_len = len(ingredient)
    food_len = len(food)

    if ingredient_len == 0:
        return food_len
    elif food_len == 0:
        return ingredient_len
        
    step_array = [[0] * (food_len + 1) for _ in range(ingredient_len + 1)]
    step_array[0][1] = 1

    for i in range(0, ingredient_len):
        step_array[i][0] = i

    for j in range(0, food_len):
        step_array[0][j] = j

    for i in range(1, ingredient_len):
        ingredient_char = ingredient[i - 1]
        for j in range(1, food_len):
            food_char = food[j - 1]

            m = 0 if ingredient_char == food_char else 1

            step_array[i][j] == min(
                min((step_array[i - 1][j] + 1), (step_array[i][j - 1] + 1)), step_array[i - 1][j - 1] + m)
        
    edit_distance = step_array[ingredient_len][food_len]
    return edit_distance

def get_all_foods():
    system = platform.system()
    if system == "Windows":
        return open('raw_data\\foodnetwork_ingredients.txt').readlines()
    else:
        return open('raw_data/foodnetwork_ingredients.txt').readlines()


print(get_nearest_food("apfel"))