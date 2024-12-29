"""
main.py
Brodie Rogers <brodie.rogers@students.cune.edu>
2024-12-5

Conway's Game of Life Simulation with Random Revival Feature.

This program simulates Conway's Game of Life using Pygame. 
Users can toggle cells alive or dead with the mouse, pause/resume the simulation, 
and observe the live cell count. Cells may randomly come to life with a small chance.

"""

import pygame
from john_conways import Grid


def handle_mouse_input(grid, cell_size):
    """
    Toggle a cell's alive state based on mouse input.

    Params:
        grid (Grid): The game grid object.
        cell_size (int): Size of each cell in pixels.
    """
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        x, y = pygame.mouse.get_pos()
        grid_x, grid_y = x // cell_size, y // cell_size
        if 0 <= grid_x < grid.width and 0 <= grid_y < grid.height:
            grid.grid[grid_x][grid_y].is_alive = not grid.grid[grid_x][grid_y].is_alive


def process_input(event, game_world, flip_flop, paused, simulation_speed):
    """
    Handle user keyboard input for controlling the simulation.

    Params:
        event (pygame.event.Event): The Pygame event to process.
        game_world (Grid): The game grid object.
        flip_flop (int): State toggle for enabling/disabling spawning.
        paused (bool): Indicates if the simulation is paused.
        simulation_speed (int): Speed of the simulation.

    Returns:
        tuple: Updated flip_flop, paused, and simulation_speed values.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            paused = not paused
        elif event.key == pygame.K_EQUALS:
            simulation_speed = min(simulation_speed + 5, 120)
        elif event.key == pygame.K_MINUS:
            simulation_speed = max(simulation_speed - 5, 5)
        elif event.key == pygame.K_s:
            if flip_flop == 1:
                game_world.spawing = False
                flip_flop = 2
            else:
                game_world.spawing = True
                flip_flop = 1
    return flip_flop, paused, simulation_speed


def render_text(screen, font, paused, simulation_speed, game_world, grid_height, grid_width, cell_size):
    """
    Render the game's status and key binding information.

    Params:
        screen (pygame.Surface): The Pygame display surface.
        font (pygame.font.Font): The font used for text rendering.
        paused (bool): Indicates if the simulation is paused.
        simulation_speed (int): Speed of the simulation.
        game_world (Grid): The game grid object.
        grid_height (int): Height of the grid in cells.
        grid_width (int): Width of the grid in cells.
        cell_size (int): Size of each cell in pixels.
    """
    text = "Paused" if paused else "Running"
    spawning = "True" if game_world.spawing else "False"
    text_surface = font.render(f"Game State: {text} | Alive: {game_world.alive_count} | Simulation Speed: {simulation_speed} | Spawning: {spawning}", True, "white")
    display_info_y = (grid_height * cell_size) - (cell_size * 70)
    screen.blit(text_surface, (display_info_y, 10))

    key_bind_text = font.render("Pause/Play: SPACE | Randomly Spawn Cells: s | Faster: = | Slower: - | Left Click: Toggle Cell", True, "white")
    info_text_height = (grid_width * cell_size) - 20
    screen.blit(key_bind_text, (display_info_y, info_text_height))


def main():
    """
    Main function to run the Conway's Game of Life simulation.
    """
    pygame.init()
    flip_flop = 1
    simulation_speed = 10
    cell_size = 8
    grid_width = 100
    grid_height = 100
    font_size = 18 if grid_width > 100 else 16
    screen = pygame.display.set_mode((grid_width * cell_size, grid_height * cell_size))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, font_size)

    game_world = Grid(grid_width, grid_height, cell_size)

    running = True
    paused = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            flip_flop, paused, simulation_speed = process_input(event, game_world, flip_flop, paused, simulation_speed)

        handle_mouse_input(game_world, cell_size)

        if not paused:
            game_world.update()

        screen.fill("black")
        game_world.draw(screen)
        render_text(screen, font, paused, simulation_speed, game_world, grid_height, grid_width, cell_size)
        pygame.display.flip()
        clock.tick(simulation_speed)

    pygame.quit()


if __name__ == "__main__":
    main()
