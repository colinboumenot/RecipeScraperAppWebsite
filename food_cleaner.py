foods = open('food_names.txt', 'r+').readlines()
backend_foodlist = open('backend_food_names.txt', "a")
print("foods len:" + str(len(foods)))
for food in range(len(foods) - 1):
    current_food = foods[food]
    if "noun" in current_food:
        current_food = current_food[:current_food.find("noun")]
        current_food.strip()
        #foodlist.append(current_food)
        backend_foodlist.write(current_food + "\n")
    else:
        foods.remove(current_food)
        food -= 1
    print(food)

#backend_foodlist.writelines(foodlist)
backend_foodlist.close()