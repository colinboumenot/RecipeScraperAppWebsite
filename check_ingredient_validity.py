import os

all_foods = open(os.path.join('raw_data', 'foodnetwork_ingredients.txt')).read().splitlines()
food_by_use = open(os.path.join('raw_data', 'frequency_list.txt')).read().splitlines()

#check if typed ingredient is a real ingredient
def check_ingredient(ingredient):
    for food in all_foods:
        if food == ingredient:
            return True
    return False

#Looks at inputed ingredient if it's not valid and finds closest match to what it should be
def get_nearest_food(ingredient:str):
    current_guess_foods = []
    current_guess_dist = 9999
    final_result = None
    for food in all_foods:
        edit_distance = check_edit_distance(ingredient, food)
        if edit_distance < current_guess_dist:
            current_guess_dist = edit_distance
            current_guess_foods.clear()
            current_guess_foods.append(food)
        elif edit_distance == current_guess_dist:
            current_guess_foods.append(food)
    for food in food_by_use:
        if food in current_guess_foods:
            final_result = food
            break
    return final_result, current_guess_dist

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

    for i in range(1, ingredient_len + 1):
        ingredient_char = ingredient[i - 1]
        for j in range(1, food_len + 1):
            food_char = food[j - 1]

            m = 0 if ingredient_char == food_char else 1

            step_array[i][j] = min(
                step_array[i - 1][j] + 1, 
                    step_array[i][j - 1] + 1, 
                    step_array[i - 1][j - 1] + m)
        
    edit_distance = step_array[ingredient_len][food_len]
    return edit_distance

print(check_edit_distance("apfel", "apple"))
print(get_nearest_food("apfel"))

def test_case_apfel():
    pass