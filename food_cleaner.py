'''
    method to clean up umbrealla food txt files
'''
def clean_umbrella_foods(filename):
    dirty_food = open(filename, 'r+').readlines()
    clean_food = open('cleaned_' + filename, "a")
    for food in range(len(dirty_food) - 1):
        current_food = dirty_food[food]
        if "[" in current_food:
            current_food = current_food[:current_food.find("[")]
            current_food.strip()
            clean_food.write(current_food + "\n")
        elif ",,,,,," == current_food:
            dirty_food.remove(current_food)
            food -= 1
        else:
            current_food = current_food[:current_food.find(",,,,,,")]
            current_food.strip()
            clean_food.write(current_food + "\n")
    clean_food.close()

'''
    create methods to convert time to minutes to keep constent on backend
    and method to go from minutes to hours for front end

    if we sorted based off of time this is something that would be used, but we don't currently have that capability
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
 