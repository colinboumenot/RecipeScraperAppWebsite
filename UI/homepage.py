import platform
import pygame
import pygame_gui
import sys

sys.path.append('.')
from check_ingredient_validity import *

# Initialize PyGame
pygame.init()


class Checkbox:
    def __init__(self, surface, x, y, idnum, color=(230, 230, 230),
        caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
        font_size=22, font_color=(0, 0, 0), 
        text_offset=(28, 1), font='Arial'):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        #identification for removal and reorganization
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self):
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 + 
        self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)
            
# Setup the display
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Recipe Creator')

# Setup UI Manager
manager = pygame_gui.UIManager(window_size)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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
input_box = search_results = back_button = filter_title = recipe_title = recipe_search_button = items_text_box = None
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
    system = platform.system()
    ingredients = []
    if system == "Windows":
        ingredients = open('raw_data\\foodnetwork_ingredients.txt').readlines()
    else:
        ingredients = open('raw_data/foodnetwork_ingredients.txt').readlines()
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

# Handling screens and transitions
def draw_filter_search_screen():
    global input_box, search_results, back_button, filter_title, items_text_box, current_screen, plus_button, minus_button
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

def draw_recipe_search_screen():
    global current_screen, back_button, recipe_title, recipe_search_button, filter_buttons
    
    title.hide()
    button_filter.hide()
    button_recipe.hide()
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 550, 100, 40),
                                               text='Back',
                                               manager=manager)
    recipe_title = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(50, 100, 300, 50),
                                                       manager=manager)
    recipe_search_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(200, 200, 200, 50),
                                                        text='Recipe Search',
                                                        manager=manager)
    
    for idx, feature in enumerate(['filter1       ', 'filter2', 'filter3']):
        btn = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(100, 300 + idx * 60, 200, 50),
                                           text=feature,
                                           manager=manager)
        filter_buttons.append(btn)
        
        # Creating checkboxes
        checkbox = Checkbox(screen, 150, 320 + idx * 60, idx, caption='', font_size=25)
        check_boxes.append(checkbox)

    current_screen = 'recipe_search'

def update_items_display():
    global delete_buttons, plus_button, minus_button, value_label, value
    formatted_text = ''
    #TODO: this is currently a bug since quantity isn't stored so it crashes the app if someone tries to add an ingredient
    for item, quantity in item_list:
        formatted_text += f'{item} - {quantity}<br>'
    items_text_box.html_text = formatted_text
    items_text_box.rebuild()

    # Remove old buttons
    for btn in delete_buttons:
        btn.kill()
    delete_buttons = []
    if plus_button:
        plus_button.kill()
    if minus_button:
        minus_button.kill()
    if value_label:
        value_label.kill()

    # Add new delete buttons
    y_offset = 0
    for idx, (item, _) in enumerate(item_list):
        btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(650, 10 + y_offset, 30, 30),
                                           text='Del',
                                           manager=manager,
                                           container=search_results,
                                           object_id=f'delete_{idx}')
        btn.item_index = idx  # Custom attribute to identify the button
        delete_buttons.append(btn)
        y_offset += 40  # Adjust y offset for next button

    # Plus Button
    plus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(370, 100, 30, 30),
                                               text='+',
                                               manager=manager,
                                               object_id=f'plus_button')

    # Value Label
    value = 0
    value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(400, 100, 30, 30),
                                              text=str(value),  # Initial value
                                              manager=manager,
                                              object_id=f'value_label')

    # Minus Button
    minus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(430, 100, 30, 30),
                                                text='-',
                                                manager=manager,
                                                object_id=f'minus_button')

def delete_item(button):
    global item_list
    if button.item_index < len(item_list):
        item_list.pop(button.item_index)
        save_user_data()
        update_items_display()

def handle_ui_events(event):
    global current_screen, item_list, value, value_label, check_boxes, recipe_search_button, input_box, item_list, items_text_box, plus_button, minus_button, value_label, filter_title, back_button, search_results
    manager.process_events(event)

    if event.type == pygame.USEREVENT:
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_filter:
                draw_filter_search_screen()
            elif event.ui_element == button_recipe:
                draw_recipe_search_screen()
            elif back_button and event.ui_element == back_button:
                title.show()
                button_filter.show()
                button_recipe.show()
                back_button.hide()
                if recipe_title:
                    recipe_title.hide()
                if recipe_search_button:
                    recipe_search_button.hide()
                for checkbox in check_boxes:
                    checkbox.checked = False
                for filter_button in filter_buttons:
                    filter_button.hide()
                current_screen = 'home'

                if input_box:
                    input_box.hide()
                item_list = []
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
                
            elif event.ui_element == plus_button:
                value += 1
                value_label.set_text(str(value))
            elif event.ui_element == minus_button:
                value -= 1
                if value < 0:
                    value = 0
                value_label.set_text(str(value))
            else:
                for btn in delete_buttons:
                    if event.ui_element == btn:
                        delete_item(btn)
                        break

        elif event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
            if event.ui_element in check_boxes:
                event.ui_element.set_text('')
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN and current_screen == 'filter_search' and input_box.get_text():
            inputted_ingredient = input_box.get_text()
            if not check_ingredient(inputted_ingredient):
                actual_ingredient = get_nearest_food(inputted_ingredient)
                #TODO: create a pop-up to ask user if actual ingredient is what they actually want
                #      if it is then update inputted_ingredeint with actual_ingredient
            item_list.append(inputted_ingredient)
            #TODO: once units and quantites are also sent in, call unit conversion method
            #update_ingredient_dict() -> uncomment once units are finalized
            save_user_data()
            update_items_display()
            input_box.set_text('')
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if current_screen == 'recipe_search':
            for box in check_boxes:
                if box.checkbox_obj.collidepoint(event.pos):
                    box.update_checkbox(event)

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
    if current_screen == 'recipe_search':
        for box in check_boxes:
            box.render_checkbox()
    pygame.display.update()

pygame.quit()