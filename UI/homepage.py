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

# Handling screens and transitions
def draw_filter_search_screen():
    global input_box, search_results, back_button, filter_title, items_text_box, current_screen
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
                                                   relative_rect=pygame.Rect(0, 0, 690, 290),
                                                   manager=manager,
                                                   container=search_results)
    input_box.focus()
    current_screen = 'filter_search'

def update_items_display():
    formatted_text = '<br>'.join(f'{item}' for item in item_list)  # Ensure correct HTML formatting
    items_text_box.html_text = formatted_text
    items_text_box.rebuild()  # Rebuild the text box to update the display

def draw_recipe_search_screen():
    global input_box, back_button, recipe_title, current_screen
    title.hide()
    button_filter.hide()
    button_recipe.hide()
    
    recipe_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(200, 50, 400, 50),
                                               text='Search Your Recipe',
                                               manager=manager)
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(50, 550, 100, 40),
                                               text='Back',
                                               manager=manager)
    input_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(50, 100, 700, 50),
                                                    manager=manager)
    current_screen = 'recipe_search'

def handle_ui_events(event):
    global current_screen, item_list
    manager.process_events(event)

    if event.type == pygame.USEREVENT:
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_filter:
                draw_filter_search_screen()
            elif event.ui_element == button_recipe:
                draw_recipe_search_screen()
            elif back_button and event.ui_element == back_button and current_screen != 'home':
                title.show()
                button_filter.show()
                button_recipe.show()
                if back_button:
                    back_button.hide()
                if input_box:
                    input_box.hide()
                if filter_title:
                    filter_title.hide()
                if recipe_title:
                    recipe_title.hide()
                if search_results:
                    search_results.hide()
                current_screen = 'home'
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN and current_screen == 'filter_search' and input_box.get_text():
            item_list.append(input_box.get_text())
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
