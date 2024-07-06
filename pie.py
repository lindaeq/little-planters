import pygame
from sys import exit

pygame.init()

coins_num = 10000

screen = pygame.display.set_mode((400, 540))
pygame.display.set_caption('pie')

# Load graphics
backdrop = pygame.image.load('graphics/planter.png')
start_button = pygame.image.load('graphics/start.png')
start_rect = start_button.get_rect(topleft=(110, 407))

forest = pygame.image.load('graphics/forest.png')
plant = pygame.image.load('graphics/plant.png')
plant_height = plant.get_height()

seeds = pygame.image.load('graphics/seeds.png')
seeds_clicked = pygame.image.load('graphics/seeds_clicked.png')
seeds_rect = seeds.get_rect(topleft=(292, 210))

pot = pygame.image.load('graphics/pot.png')
pot_clicked = pygame.image.load('graphics/pot_clicked.png')
pot_rect = pot.get_rect(topleft=(292, 305))

blank_pot = pygame.image.load('graphics/blank_pot.png')
blank_pot_height = blank_pot.get_height()

# Load fonts
font = pygame.font.Font(None, 24)

# Grid dimensions and positions
num_columns = 3
num_rows = 3
cell_width = 75
cell_height = 100
grid_x = 35
grid_y = 210

# Track the current screen and selection states
current_screen = 'main'
seeds_selected = False
pot_selected = False

# Initial grid setup
grid = [['empty' for _ in range(num_columns)] for _ in range(num_rows)]
# Assume bottom row has pots
for col in range(num_columns):
    grid[num_rows - 1][col] = 'blank_pot'

tasks = [
    ("Recycle 5 items", "Recycling one aluminum can saves enough energy to run a TV for three hours."),
    ("Plant a tree", "Trees can cool a city by up to 1O°F by shading our homes and streets."),
    ("Use a reusable bag", "One reusable bag can save over 7OO plastic bags from being used."),
    ("Save 1O liters of water", "Fixing a leaky faucet can save up to 1O, OOO liters of water a year."),
    ("Bike to work", "Biking to work can reduce greenhouse gas emissions by over 75%."),
    ("Turn off lights", "Turning off lights when not in use can save up to $1OO a year on electricity."),
    ("Use a reusable bottle", "A reusable bottle can save an average of 156 plastic bottles annually."),
    ("Take shorter showers", "Shortening your shower by just 1-2 minutes can save up to 15O gallons per month."),
    ("Compost food waste", "Composting can reduce the amount of waste sent to landfills by up to 3O%."),
    ("Carpool with friends", "Carpooling can cut your carbon footprint by half."),
    ("Buy local produce", "Buying local reduces your carbon footprint and supports local farmers."),
    ("Use energy-efficient bulbs", "LED bulbs use up to 8O% less energy than traditional bulbs."),
    ("Unplug devices", "Unplugging devices when not in use can save up to $2OO a year."),
    ("Eat a plant-based meal", "Skipping one meat-based meal per week can save the equivalent of driving 1,16O miles."),
    ("Wash clothes in cold water", "Washing clothes in cold water can save up to 9O% of the energy used for heating."),
    ("Dry clothes on a line", "Line drying can save your household more than $1OO annually."),
    ("Install a low-flow showerhead", "Low-flow showerheads can reduce water usage by 4O% or more."),
    ("Reduce, reuse, recycle", "Recycling just one ton of paper saves 17 trees."),
    ("Use a programmable thermostat", "A programmable thermostat can save up to 1O% on heating and cooling costs."),
    ("Avoid single-use plastics", "Using a reusable straw can save over 5OO straws from being used annually.")
]

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines

while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == 'main' and start_rect.collidepoint(event.pos):
                current_screen = 'forest'
            elif current_screen == 'forest':
                if seeds_rect.collidepoint(event.pos):
                    seeds_selected = not seeds_selected
                    pot_selected = False
                elif pot_rect.collidepoint(event.pos):
                    pot_selected = not pot_selected
                    seeds_selected = False
                else:
                    for row in range(num_rows):
                        for col in range(num_columns):
                            cell_rect = pygame.Rect(grid_x + col * cell_width, grid_y + row * cell_height, cell_width, cell_height)
                            if cell_rect.collidepoint(event.pos):
                                if seeds_selected and grid[row][col] == 'blank_pot':
                                    grid[row][col] = 'plant'
                                    seeds_selected = False
                                elif pot_selected and grid[row][col] == 'empty':
                                    grid[row][col] = 'blank_pot'
                                    pot_selected = False

    if current_screen == 'main':
        screen.blit(backdrop, (0, 0))
        screen.blit(start_button, (110, 407))
    
    elif current_screen == 'forest':
        screen.blit(forest, (0, 0))
        screen.blit(seeds_clicked if seeds_selected else seeds, seeds_rect.topleft)
        screen.blit(pot_clicked if pot_selected else pot, pot_rect.topleft)
        
        for row in range(num_rows):
            for col in range(num_columns):
                cell_rect = pygame.Rect(grid_x + col * cell_width, grid_y + row * cell_height, cell_width, cell_height)

                pygame.draw.rect(screen, (225, 225, 225), cell_rect, 1)
                
                # Highlight cells on hover and draw contents (pot or plant)
                for row in range(num_rows):
                    for col in range(num_columns):
                        cell_rect = pygame.Rect(grid_x + col * cell_width, grid_y + row * cell_height, cell_width, cell_height)
                        # Draw grid border
                        pygame.draw.rect(screen, (225, 225, 225), cell_rect, 1)
                        
                        # Draw contents (pot or plant)
                        if grid[row][col] == 'plant':
                            pot_x = cell_rect.centerx - blank_pot.get_width() // 2
                            pot_y = cell_rect.bottom - blank_pot_height  # Bottom align the pot
                            plant_x = cell_rect.centerx - plant.get_width() // 2
                            plant_y = cell_rect.centery - plant_height // 2 - 10  # Adjust to touch the top of the pot
                            
                            # Draw plant first (behind pot)
                            screen.blit(plant, (plant_x, plant_y))
                            # Then draw pot
                            screen.blit(blank_pot, (pot_x, pot_y))
                        
                        elif grid[row][col] == 'blank_pot':
                            pot_x = cell_rect.centerx - blank_pot.get_width() // 2
                            pot_y = cell_rect.bottom - blank_pot_height  # Bottom align the pot
                            screen.blit(blank_pot, (pot_x, pot_y))
                        
                        # Highlight cells on hover
                        if cell_rect.collidepoint(mouse_pos):
                            if pot_selected and grid[row][col] == 'empty':
                                overlay_rect = cell_rect.inflate(-10, -10)
                                pygame.draw.rect(screen, (0, 255, 0, 128), overlay_rect)  # Light green transparent overlay
                                text = "add a pot"
                                text_surface = font.render(text, True, (0, 0, 0))
                                text_rect = text_surface.get_rect(center=overlay_rect.center)
                                
                                # Check if the text exceeds cell boundaries horizontally
                                if text_rect.width > overlay_rect.width:
                                    # Wrap the text
                                    lines = []
                                    words = text.split()
                                    current_line = ''
                                    
                                    for word in words:
                                        test_line = current_line + word + ' '
                                        test_rect = font.render(test_line, True, (0, 0, 0)).get_rect()
                                        
                                        if test_rect.width <= overlay_rect.width:
                                            current_line = test_line
                                        else:
                                            lines.append(current_line)
                                            current_line = word + ' '
                                    
                                    lines.append(current_line)
                                    
                                    # Render wrapped text
                                    text_surfaces = [font.render(line, True, (0, 0, 0)) for line in lines]
                                    total_height = sum(surface.get_height() for surface in text_surfaces)
                                    
                                    y_offset = overlay_rect.centery - total_height / 2
                                    
                                    for idx, surface in enumerate(text_surfaces):
                                        text_rect = surface.get_rect(centerx=overlay_rect.centerx, y=y_offset + idx * surface.get_height())
                                        screen.blit(surface, text_rect)
                                else:
                                    screen.blit(text_surface, text_rect)
                                
                            elif seeds_selected and grid[row][col] == 'blank_pot':
                                overlay_rect = cell_rect.inflate(-10, -10)
                                pygame.draw.rect(screen, (0, 255, 0, 128), overlay_rect)  # Light green transparent overlay
                                text = "plant a plant"
                                text_surface = font.render(text, True, (0, 0, 0))
                                text_rect = text_surface.get_rect(center=overlay_rect.center)
                                
                                # Check if the text exceeds cell boundaries horizontally
                                if text_rect.width > overlay_rect.width:
                                    # Wrap the text
                                    lines = []
                                    words = text.split()
                                    current_line = ''
                                    
                                    for word in words:
                                        test_line = current_line + word + ' '
                                        test_rect = font.render(test_line, True, (0, 0, 0)).get_rect()
                                        
                                        if test_rect.width <= overlay_rect.width:
                                            current_line = test_line
                                        else:
                                            lines.append(current_line)
                                            current_line = word + ' '
                                    
                                    lines.append(current_line)
                                    
                                    # Render wrapped text
                                    text_surfaces = [font.render(line, True, (0, 0, 0)) for line in lines]
                                    total_height = sum(surface.get_height() for surface in text_surfaces)
                                    
                                    y_offset = overlay_rect.centery - total_height / 2
                                    
                                    for idx, surface in enumerate(text_surfaces):
                                        text_rect = surface.get_rect(centerx=overlay_rect.centerx, y=y_offset + idx * surface.get_height())
                                        screen.blit(surface, text_rect)
                                else:
                                    screen.blit(text_surface, text_rect)


    pygame.display.update()
