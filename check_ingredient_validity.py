#check if typed ingredient is a real ingredient
def check_ingredient(self, ingredient):
    all_foods = open('raw_data\\foodnetwork_ingredients.txt').readlines() #may cause issues if user has mac, will test later
    for food in all_foods:
        if food == ingredient:
            return True
    return False

def check_edit_distance(self, ingredient):
    
    pass