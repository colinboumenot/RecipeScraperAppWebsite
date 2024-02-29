class Recipe:
    def __init__(self, title, time, servings, diffuculty, ingredients, steps, tags):
        self.title = title
        self.time = time
        self.servings = servings
        self.difficulty = diffuculty
        self.ingredients = ingredients
        self.steps = steps
        self.tags = tags

    #TODO: create method within Recipe to convert 
    #     ingerdients from list to dictionary {amount:ingredient}
    

    '''
    create methods to convert time to minutes to keep constent on backend
    and method to go from minutes to hours for front end
    '''
    def time_to_minutes(self):
        for time in self.time:
            if "hr" in time:
                time.lower()
                split_index = time.index("hr")
                hr = time[:split_index - 1].strip()
                min = time[split_index + 2:].strip()
                time = int(hr)*60 + int(min)

    def minutes_to_time(self):
        for time in self.time:
            if time > 60:
                hr = int(time/60)
                min = int(time%60)
                time = hr + " hr " + min + " min"


