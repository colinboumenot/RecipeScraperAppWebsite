class Recipe:
    def __init__(self, title, time, servings, diffuculty, ingredients, steps, tags):
        self.title = title
        self.time = time
        self.servings = servings
        self.difficulty = diffuculty
        self.ingredients = ingredients
        self.ingredients_backend_side = ingredients
        self.steps = steps
        self.tags = tags
    
    def set_ingredients_backend_side(self, ingredients):
        self.ingredients_backend_side = ingredients



