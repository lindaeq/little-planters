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

while True:
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
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)
                if grid[row][col] == 'plant':
                    plant_x = cell_rect.centerx - plant.get_width() // 2
                    plant_y = cell_rect.centery - plant_height // 2 - 10  # Adjust to touch the top of the pot
                    screen.blit(plant, (plant_x, plant_y))
                    pot_x = cell_rect.centerx - blank_pot.get_width() // 2
                    pot_y = cell_rect.bottom - blank_pot_height  # Bottom align the pot
                    screen.blit(blank_pot, (pot_x, pot_y))
                elif grid[row][col] == 'blank_pot':
                    pot_x = cell_rect.centerx - blank_pot.get_width() // 2
                    pot_y = cell_rect.bottom - blank_pot_height  # Bottom align the pot
                    screen.blit(blank_pot, (pot_x, pot_y))

    pygame.display.update()
