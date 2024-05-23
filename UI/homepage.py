import pygame
import pygame_gui

# Initialize PyGame
pygame.init()

# Setup the display
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Recipe Creator')

# Setup UI Manager
manager = pygame_gui.UIManager(window_size)

# Define colors
WHITE = (255, 255, 255)

# UI Components
def create_home_screen():
    """Create components for the home screen."""
    title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(200, 50, 400, 50),
                                        text='Recipe Creator',
                                        manager=manager)
    button_filter = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(300, 150, 200, 50),
                                                 text='Filter Search',
                                                 manager=manager)
    button_recipe = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(300, 250, 200, 50),
                                                 text='Recipe Search',
                                                 manager=manager)
    return title, button_filter, button_recipe

title, button_filter, button_recipe = create_home_screen()

# Screen state
current_screen = 'home'
input_box = search_results = back_button = filter_title = recipe_title = items_text_box = None
item_list = []
delete_buttons = []

#write information item_list to file
def save_user_data():
    user_ingredients = open('user_ingredients.txt', "w")
    user_ingredients.truncate(0)
    for ingredient in item_list:
        user_ingredients.write(ingredient + "\n") #once units and quantities are added change to write(ingredient + "%" + quantity + "%" + unit + "\n")
    user_ingredients.close()

#check to see if user_ingredients.txt is empty, and if not add to item_list upon opening the app
def check_saved_data():
    user_ingredients = []
    try:
        user_ingredients = open('user_ingredients.txt', "x").readlines()
    except:
        print("file already exists")
        user_ingredients = open('user_ingredients.txt', "r").readlines()

    if user_ingredients is not None:
        for ingredient in user_ingredients:
            food_amount_unit = ingredient.split('%')
            if food_amount_unit[0] not in item_list:
                item_list.append(food_amount_unit[0].strip("\n"))

check_saved_data()
save_user_data()

#initalize empty dictionary with all ingredients
def create_ingredient_dict():
    ingredient_dict = dict()
    ingredients = open('raw_data\\foodnetwork_ingredients.txt').readlines() #may cause issues if user has mac, will test later
    for food in ingredients:
        food = food[0:len(food) - 1] #removes the \n seen at the end of foods
        ingredient_dict[food] = [0, 0, 0, 0]
    return ingredient_dict

ingredient_dict = create_ingredient_dict()

def update_ingredient_dict():
    user_ingredients = open('user_ingredients.txt', "r").readlines()
    for ingredient in user_ingredients:
        ingredient = ingredient.split("%")
        food = ingredient[0]
        amount = ingredient[1]
        unit = ingredient[2]
        if unit == "grams": 
            ingredient_dict[food][0] = amount
        elif unit == "cups":
            ingredient_dict[food][1] = amount
        elif unit == "packages":
            ingredient_dict[food][2] = amount
        elif unit == "wholes":
            ingredient_dict[food][3] = amount
        else: #for foods without a amount that needs to be specified, like salt
            ingredient_dict[food] = [9999, 9999, 9999, 9999]

# Handling screens and transitions
def draw_filter_search_screen():
    global input_box, search_results, back_button, filter_title, items_text_box, current_screen, delete_buttons
    title.hide()
    button_filter.hide()
    button_recipe.hide()

    filter_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(200, 50, 400, 50),
                                               text='List out your ingredients',
                                               manager=manager)
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 550, 100, 40),
                                               text='Back',
                                               manager=manager)
    input_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(50, 100, 300, 50),
                                                    manager=manager)
    search_results = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(50, 160, 700, 300),
                                                 manager=manager)
    items_text_box = pygame_gui.elements.UITextBox(html_text='',
                                                   relative_rect=pygame.Rect(0, 0, 640, 290),
                                                   manager=manager,
                                                   container=search_results)
    input_box.focus()
    current_screen = 'filter_search'
    update_items_display()

def update_items_display():
    global delete_buttons
    formatted_text = '<br>'.join(f'{item}' for item in item_list)
    items_text_box.html_text = formatted_text
    items_text_box.rebuild()

    # Remove old buttons
    for btn in delete_buttons:
        btn.kill()
    delete_buttons = []

    # Add new delete buttons
    y_offset = 0
    for idx, item in enumerate(item_list):
        btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(650, 10 + y_offset, 30, 30),
                                           text='Del',
                                           manager=manager,
                                           container=search_results,
                                           object_id=f'delete_{idx}')
        btn.item_index = idx  # Custom attribute to identify the button
        delete_buttons.append(btn)
        y_offset += 40  # Adjust y offset for next button

def delete_item(button):
    global item_list
    if button.item_index < len(item_list):
        item_list.pop(button.item_index)
        save_user_data()
        update_items_display()

def handle_ui_events(event):
    global current_screen, item_list
    manager.process_events(event)

    if event.type == pygame.USEREVENT:
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_filter:
                draw_filter_search_screen()
            elif event.ui_element == button_recipe:
                #draw_recipe_search_screen()
                pass
            elif back_button and event.ui_element == back_button:
                title.show()
                button_filter.show()
                button_recipe.show()
                back_button.hide()
                input_box.hide()
                filter_title.hide()
                if recipe_title:
                    recipe_title.hide()
                search_results.hide()
                current_screen = 'home'
            else:
    
                for btn in delete_buttons:
                    if event.ui_element == btn:
                        delete_item(btn)
                        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN and current_screen == 'filter_search' and input_box.get_text():
            item_list.append(input_box.get_text())
            #TODO: once units and quantites are also sent in, call unit conversion method
            #update_ingredient_dict() -> uncomment once units are finalized
            save_user_data()
            update_items_display()
            input_box.set_text('')

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handle_ui_events(event)

    manager.update(time_delta)

    screen.fill(WHITE)
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()
