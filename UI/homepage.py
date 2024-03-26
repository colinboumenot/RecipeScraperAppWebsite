import pygame
import pygame_gui

pygame.init()

window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Pygame UI')

ui_manager = pygame_gui.UIManager(window_size)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

button_width = 200
button_height = 50
button_x = (window_size[0] - button_width) // 2
button_y = 100
button_gap = 20


button_recipe_creator = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((button_x, button_y), (button_width, button_height)),
    text='Recipe Creator',
    manager=ui_manager
)

button_filter_search = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((button_x, button_y + button_height + button_gap), (button_width // 2 - button_gap // 2, button_height)),
    text='Filter Search',
    manager=ui_manager
)

button_recipe_search = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((button_x + button_width // 2 + button_gap // 2, button_y + button_height + button_gap), (button_width // 2 - button_gap // 2, button_height)),
    text='Recipe Search',
    manager=ui_manager
)

# Input fields for search buttons
##input_field_filter_search = pygame_gui.elements.UITextEntryLine(
    ##relative_rect=pygame.Rect((button_x, button_y + 2 * (button_height + button_gap)), (button_width // 2 - button_gap // 2, button_height)),
    ##manager=ui_manager
)

##input_field_recipe_search = pygame_gui.elements.UITextEntryLine(
  ##  relative_rect=pygame.Rect((button_x + button_width // 2 + button_gap // 2, button_y + 2 * (button_height + button_gap)), (button_width // 2 - button_gap // 2, button_height)),
    ##manager=ui_manager
)

# Main loop
is_running = True
clock = pygame.time.Clock()

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_filter_search:
                    #input_field_filter_search.show()
                elif event.ui_element == button_recipe_search:
                    input_field_recipe_search.show()
#
        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    window.fill(WHITE)

    ui_manager.draw_ui(window)

    pygame.display.update()

pygame.quit()