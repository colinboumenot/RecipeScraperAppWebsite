
import platform
import pygame
import pygame_gui

import sys
import os

import pickle


sys.path.append('.')
from check_ingredient_validity import *
from find_recipes import find_recipes_no_quantities, find_recipes_no_quantities_exclusive
from recipe import Recipe

# Initialize PyGame
pygame.init()

# Initialize the mixer for sounds
pygame.mixer.init()

# Initialize fonts
all_fonts = pygame.font.get_fonts() 

# Load sounds
hover_sound = pygame.mixer.Sound("hover_sound.wav")
click_sound = pygame.mixer.Sound("click_sound.wav")

class Checkbox:
    def __init__(self, surface, x, y, caption, manager, size=20, font_size=22):
        self.surface = surface
        self.x = x
        self.y = y
        self.size = size
        self.caption = caption
        self.manager = manager
        self.font_size = font_size
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.checked = False

    def render_checkbox(self):
        # Draw the checkbox
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(self.surface, (255, 255, 255), rect)
        pygame.draw.rect(self.surface, (0, 0, 0), rect, 2)
        
        # Draw the check mark if the box is checked
        if self.checked:
            pygame.draw.line(self.surface, (0, 0, 0), (self.x, self.y), (self.x + self.size, self.y + self.size), 2)
            pygame.draw.line(self.surface, (0, 0, 0), (self.x, self.y + self.size), (self.x + self.size, self.y), 2)
        
        # Render the caption
        caption_surface = self.font.render(self.caption, True, (0, 0, 0))
        self.surface.blit(caption_surface, (self.x + self.size + 5, self.y))

    def update_checkbox(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            rect = pygame.Rect(self.x, self.y, self.size, self.size)
            if rect.collidepoint(mouse_pos):
                self.checked = not self.checked
                return True
            return False

# Setup the display
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Recipe Creator')

# Setup UI Manager - dig more into to figure out the scroll
manager = pygame_gui.UIManager(window_size)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load background image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, window_size)

# UI Components
def create_home_screen():
    """Create components for the home screen."""
    title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(200, 50, 400, 80),
                                        text='Recipe Creator', 
                                        manager=manager)
    button_filter = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(300, 200, 200, 60),
                                                 text='Search With Ingredients',
                                                 manager=manager)
    button_recipe = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(300, 300, 200, 60),
                                                 text='Search With Recipe',
                                                 manager=manager)
    # button_ingredients = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(300, 400, 200, 60),
    #                                                   text='Food Ingredients',
    #                                                   manager=manager)
    return title, button_filter, button_recipe

title, button_filter, button_recipe = create_home_screen()

# Screen state
current_screen = 'home'
input_box = search_results = back_button = filter_title = recipe_title = recipe_search_button = items_text_box = ingredients_text_box = extra_button = filter_checkbox = search_box = up_button = down_button = recipe_text_box = None
item_list = []
delete_buttons = []
recipe_buttons = []

#write information item_list to file
def save_user_data():
    user_ingredients = open('user_ingredients.txt', "w")
    for ingredient, quantity in item_list:
        user_ingredients.write(f"{ingredient}%{quantity}\n")
    user_ingredients.close()
# Flags to control sound playback
hovered_element = None
hovered_element_prev = None

# Check to see if user_ingredients.txt is empty, and if not add to item_list upon opening the app
def check_saved_data():
    user_ingredients = []
    try:
        user_ingredients = open('user_ingredients.txt', "x").read().splitlines()
    except:
        print("file already exists")
        user_ingredients = open('user_ingredients.txt', "r").read().splitlines()

    if user_ingredients is not None:
        for ingredient in user_ingredients:
            food_amount_unit = ingredient.split('%')
            item_list_tuple = (food_amount_unit[0], food_amount_unit[1])
            if item_list_tuple not in item_list:
                item_list.append(item_list_tuple)

check_saved_data()
save_user_data()

# Initialize empty dictionary with all ingredients
def create_ingredient_dict():
    ingredient_dict = dict()
    ingredients = []
    ingredients = open(os.path.join('raw_data', 'foodnetwork_ingredients.txt')).read().splitlines()
    for food in ingredients:
        ingredient_dict[food] = [0, 0, 0, 0]
    return ingredient_dict

ingredient_dict = create_ingredient_dict()

'''
    NOTE: since there's currently no units the ingredient_dict
    is going to be made off of the assumption that there is an infinite amount of each ingredient adeded
    
    However in theory is should work automatically once units are added, once they're been changed to match
    the general syntax of user_ingredients.txt
'''
def ingredient_dict_addition():
    user_ingredients = open('user_ingredients.txt', "r").read().splitlines()
    for ingredient in user_ingredients:
        ingredient = ingredient.split("%")
        food = ingredient[0]
        amount = ingredient[1]
        try:
            unit = ingredient[2]
        except: #since units aren't currently given this should stop any potential out of range errors
            unit = None
        if unit == "grams": 
            ingredient_dict[food][0] = amount
        elif unit == "cups":
            ingredient_dict[food][1] = amount
        elif unit == "packages":
            ingredient_dict[food][2] = amount
        elif unit == "wholes":
            ingredient_dict[food][3] = amount
        else:
            ingredient_dict[food] = [9999, 9999, 9999, 9999]

def ingredient_dict_deletion():
    user_ingredients = open('user_ingredients.txt', "r").read().splitlines()
    stored_foods = ingredient_dict.keys()
    user_foods = []
    for ingredient in user_ingredients:
        ingredient = ingredient.split("%")
        user_foods.append(ingredient[0])
    for food in stored_foods:
        if food not in user_foods:
            ingredient_dict[food] = [0, 0, 0, 0]

#takes all recipes that use parmigiano as an ingredient (there's 87) and returns as a list
def create_test_recipies():
    with open('raw_data/pickle_files/ingredient_to_recipes_dict.pickle', 'rb') as f:
        ingredient_to_recipes = pickle.load(f)
    test_recipes = ingredient_to_recipes['parmigiano']
    return test_recipes

test_recipies = list(create_test_recipies())

# Plus Button
plus_button = None

# Minus Button
minus_button = None

# Value
value = 0

# Value Label
value_label = None

# Checkboxes
check_boxes = []

filter_buttons = []

#x - count for scrolling down
x = 0
exclusive_ingredient_search_on = True
max_len = 0

def get_final_recipe():
    user_foods = []
    user_ingredients = open('user_ingredients.txt', "r").read().splitlines()
    for ingredient in user_ingredients:
        ingredient = ingredient.split("%")
        food = ingredient[0]
        user_foods.append(food)
    if exclusive_ingredient_search_on:
       return find_recipes_no_quantities_exclusive(ingredient_dict)
    return find_recipes_no_quantities(user_foods, ingredient_dict)

def draw_searched_screen():
    global current_screen, back_button, ingredients_text_box, recipe_buttons, up_button, down_button, max_len
    title.hide()
    button_filter.hide()
    button_recipe.hide()
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 550, 100, 40),
                                               text='Back',
                                               manager=manager)
    
    final_recepies = get_final_recipe()
    print(final_recepies)
    final_recepies = test_recipies
    max_len = len(final_recepies)
    up_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(80, 100, 60, 60),
                                               text='UP',
                                               manager=manager)
    down_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(80, 440, 60, 60),
                                               text='DOWN',
                                               manager=manager)
    y = 0
    for i in range(5 * x , min(5 * (x + 1), len(final_recepies))):
        btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(200, 40 + y * 100, 500, 70),
                                               text=final_recepies[i].title,
                                               manager=manager)
        y += 1
        recipe_buttons.append([btn, final_recepies[i]])
                        
    current_screen = 'searched screen'
    

def draw_recipe_screen(recipe):
    global current_screen, back_button, ingredients_text_box, recipe_buttons, up_button, down_button, max_len, recipe_text_box
    title.hide()
    button_filter.hide()
    button_recipe.hide()
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 550, 100, 40),
                                               text='Back',
                                               manager=manager)
    recipe_text_box = pygame_gui.elements.UITextBox(html_text='',
                                                relative_rect=pygame.Rect(50, 100, 700, 400),
                                                manager=manager)
    recipe_text = recipe.title + '\n' 
    recipe_text += str(recipe.time) + '\n'
    recipe_text += str(recipe.servings) + '\n'
    recipe_text += str(recipe.difficulty) + '\n\n' 
    recipe_text += '\n'.join(recipe.ingredients) + '\n\n' 
    recipe_text += '\n'.join(recipe.steps)
    recipe_text_box.html_text = recipe_text
    recipe_text_box.rebuild()


# Handling screens and transitions
def draw_filter_search_screen():
    global input_box, search_results, back_button, filter_title, items_text_box, current_screen, plus_button, minus_button, value_label, extra_button, filter_checkbox, search_box
    title.hide()
    button_filter.hide()
    button_recipe.hide()
    #button_ingredients.hide()

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
    plus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(370, 100, 30, 30),
                                               text='+',
                                               manager=manager,
                                               object_id=f'plus_button')
    value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(400, 100, 30, 30),
                                              text=str(value),
                                              manager=manager,
                                              object_id=f'value_label')
    minus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(430, 100, 30, 30),
                                                text='-',
                                                manager=manager,
                                                object_id=f'minus_button')
    
    filter_checkbox = Checkbox(screen, 50, 500, 'Include all recipies containing this ingredient', manager)
    
    extra_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(650, 550, 100, 40),
                                                text='Search',
                                                manager=manager)
    # Sorry my naming convention sucks, thought It'll be confusing if I named it search button
    # search_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(650, 500, 100, 40),
    #                                                  manager=manager)
    
    input_box.focus()
    current_screen = 'filter_search'
    items_text_box.html_text = ''
    items_text_box.rebuild()
    update_items_display()

def draw_recipe_search_screen():
    global current_screen, back_button, recipe_title, recipe_search_button, check_boxes
    title.hide()
    button_filter.hide()
    button_recipe.hide()
    #button_ingredients.hide()
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 550, 100, 40),
                                               text='Back',
                                               manager=manager)
    recipe_title = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(50, 100, 300, 50),
                                                       manager=manager)
    recipe_search_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(200, 200, 200, 50),
                                                        text='Search',
                                                        manager=manager)
    check_boxes = [
        Checkbox(screen, 100, 300, 'Veg', manager),
        Checkbox(screen, 100, 360, 'Non Veg', manager),
        Checkbox(screen, 100, 420, 'Chicken', manager)
    ]

    current_screen = 'recipe_search'

def draw_autocorrect_popup(correction):
    pop_up_screen = pygame.draw.rect(screen, BLACK, pygame.Rect(290, 200, 160, 100)) 
    autocorrect_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(300, 210, 130, 20), 
                                               text='Did you mean to type ' + correction + '?',
                                               manager=manager)
    yes_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(380, 275, 50, 15), 
                                               text='Yes',
                                               manager=manager)
    no_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(295, 275, 50, 15), 
                                               text='No',
                                               manager=manager)
    
    pass
# def draw_ingredients_screen():
#     global current_screen, back_button, ingredients_text_box
#     title.hide()
#     button_filter.hide()
#     button_recipe.hide()
#     button_ingredients.hide()
#     back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 550, 100, 40),
#                                                text='Back',
#                                                manager=manager)
#     ingredients_text_box = pygame_gui.elements.UITextBox(html_text='',
#                                                          relative_rect=pygame.Rect(50, 100, 700, 400),
#                                                          manager=manager)
    # ingredients_text = ''
    # with open('foodnetwork_ingredients.txt', 'r') as file:
    #     ingredients_text = file.read().replace('\n', '<br>')

    # ingredients_text_box.html_text = ingredients_text
    # ingredients_text_box.rebuild()
    # current_screen = 'ingredients'

def update_items_display():
    global delete_buttons, plus_button, minus_button, value_label, value
    formatted_text = ''
    for item, quantity in item_list:
        formatted_text += f'{item} - {quantity}<br>'
    items_text_box.html_text = formatted_text
    items_text_box.rebuild()

    for btn in delete_buttons:
        btn.kill()
    delete_buttons = []
    if plus_button:
        plus_button.kill()
    if minus_button:
        minus_button.kill()
    if value_label:
        value_label.kill()

    y_offset = 0
    for idx, (item, _) in enumerate(item_list):
        btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(650, 10 + y_offset, 30, 30),
                                           text='Del',
                                           manager=manager,
                                           container=search_results,
                                           object_id=f'delete_{idx}')
        btn.item_index = idx
        delete_buttons.append(btn)
        y_offset += 40

    plus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(370, 100, 30, 30),
                                               text='+',
                                               manager=manager,
                                               object_id=f'plus_button')

    value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(400, 100, 30, 30),
                                              text=str(value),
                                              manager=manager,
                                              object_id=f'value_label')

    minus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(430, 100, 30, 30),
                                                text='-',
                                                manager=manager,
                                                object_id=f'minus_button')

def delete_item(button):
    global item_list
    if button.item_index < len(item_list):
        item_list.pop(button.item_index)
        save_user_data()
        ingredient_dict_deletion()
        update_items_display()

def handle_ui_events(event):
    global current_screen, item_list, value, value_label, check_boxes, recipe_search_button, input_box, items_text_box, plus_button
    global  minus_button, value_label, filter_title, back_button, search_results, ingredients_text_box, extra_button, filter_checkbox, search_box
    global hovered_element, hovered_element_prev
    global exclusive_ingredient_search_on
    global up_button, down_button
    global x

    manager.process_events(event)

    if event.type == pygame.USEREVENT:
        if hasattr(event, 'user_type'):
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                click_sound.play()
                if event.ui_element == button_filter:
                    draw_filter_search_screen()
                elif event.ui_element == button_recipe:
                    draw_recipe_search_screen()
                #elif event.ui_element == button_ingredients:
                    #draw_ingredients_screen()
                elif event.ui_element == extra_button:
                    back_button.hide()
                    extra_button.hide()
                    filter_title.hide()
                    input_box.hide()
                    search_results.hide()
                    items_text_box.hide()
                    plus_button.hide()
                    value_label.hide()
                    minus_button.hide()
                    extra_button.hide()
                    draw_searched_screen()
                elif event.ui_element == up_button:
                    if x != 0:
                        x -= 1
                    for btn in recipe_buttons:
                        btn[0].hide()
                    back_button.hide()
                    up_button.kill()
                    down_button.kill()
                    draw_searched_screen()
                elif event.ui_element == down_button:
                    if 5 * (x + 1) <= max_len:
                        x += 1
                    for btn in recipe_buttons:
                        btn[0].hide()
                    back_button.hide()
                    up_button.kill()
                    down_button.kill()
                    draw_searched_screen()
                elif back_button and event.ui_element == back_button:
                    title.show()
                    button_filter.show()
                    button_recipe.show()
                    #button_ingredients.show()
                    back_button.hide()
                    if recipe_title:
                        recipe_title.hide()
                    if recipe_search_button:
                        recipe_search_button.hide()
                    if ingredients_text_box:
                        ingredients_text_box.hide()
                    if extra_button:
                        extra_button.hide()
                    if search_box:
                        search_box.hide()
                    for checkbox in check_boxes:
                        checkbox.checked = False
                    current_screen = 'home'
                    for btn in recipe_buttons:
                        if btn[0]:
                            btn[0].hide()
                    if up_button:
                        up_button.hide()
                    if down_button:
                        down_button.hide()

                    if input_box:
                        input_box.hide()
                    if items_text_box:
                        items_text_box.hide()
                    if plus_button:
                        plus_button.hide()
                    if minus_button:
                        minus_button.hide()
                    if value_label:
                        value_label.hide()
                    if filter_title:
                        filter_title.hide()
                    back_button.hide()
                    if search_results:
                        search_results.hide()
                    if recipe_text_box:
                        recipe_text_box.hide()

                elif event.ui_element == plus_button:
                    value += 1
                    value_label.set_text(str(value))
                elif event.ui_element == minus_button:
                    value -= 1
                    if value < 0:
                        value = 0
                    value_label.set_text(str(value))
                else:
                    for btn in recipe_buttons:
                        if event.ui_element == btn[0]:
                            for btn1 in recipe_buttons:
                                btn1[0].hide()
                            back_button.hide()
                            up_button.kill()
                            down_button.kill()
                            draw_recipe_screen(btn[1])
                    for btn in delete_buttons:
                        if event.ui_element == btn:
                            delete_item(btn)
                            break

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN and current_screen == 'filter_search' and input_box.get_text():
            inputted_ingredient = input_box.get_text()

            if not check_ingredient(inputted_ingredient):
                actual_ingredient = get_nearest_food(inputted_ingredient)
                draw_autocorrect_popup(actual_ingredient) #TODO: add point for searching for 
            item_list.append((inputted_ingredient, value))
            #TODO: once units are added remember to call unit conversion method
            ingredient_dict_addition()

            save_user_data()
            update_items_display()
            input_box.set_text('')
            value = 0  # Reset value to 0 after adding the ingredient
            value_label.set_text(str(value))
            # Update value label to reflect reset value

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if current_screen == 'recipe_search':
            for checkbox in check_boxes:
                checkbox.update_checkbox(event)
        elif current_screen == 'filter_search':
            flag = filter_checkbox.update_checkbox(event)
            if filter_checkbox.checked:
                exclusive_ingredient_search_on = False
            else:
                exclusive_ingredient_search_on = True


    elif event.type == pygame.MOUSEMOTION:
        for element in [button_filter, button_recipe, plus_button, minus_button, back_button, extra_button]:
            if element is not None and element.is_focused:
                hovered_element = element
                break
        else:
            hovered_element = None

        if hovered_element != hovered_element_prev:
            if hovered_element is not None:
                hover_sound.play()
            hovered_element_prev = hovered_element

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
    screen.blit(background_image, (0, 0))
    manager.draw_ui(screen)
    if current_screen == 'recipe_search':
        for checkbox in check_boxes:
            checkbox.render_checkbox()
    elif current_screen == 'filter_search':
        filter_checkbox.render_checkbox()
    pygame.display.update()

pygame.quit()
