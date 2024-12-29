"""
john_conways.py
Brodie Rogers <brodie.rogers@students.cune.edu>
2024-12-5

Conway's Game of Life Grid and Cell Classes.

This module contains the `Cell` and `Grid` classes used in the Conway's Game of Life simulation. 
The `Cell` class represents individual cells in the grid, while the `Grid` class handles 
the overall structure, rendering, and updates of the game grid.


"""

import pygame
import random



class Cell:
    """
    Represents a single cell in the grid.

    Attributes:
        is_alive (bool): Indicates whether the cell is alive or dead.
        is_sick (bool): Indicates whether the cell is sick, with a random chance of being true.
    """
    
    def __init__(self, is_alive=False):
        """
        Initialize a cell.

        Args:
            is_alive (bool): The state of the cell (alive or dead).
        """
        self.is_alive = is_alive


    def check_neighbors(self, grid, x, y):
        """
        Count the number of alive neighbors for this cell.

        Params:
            grid (list of list of Cell): The game grid.
            x (int): The x-coordinate of this cell.
            y (int): The y-coordinate of this cell.

        Returns:
            int: The count of alive neighboring cells.
        """
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny].is_alive:
                    count += 1
        return count


class Grid:
    """
    Represents the game grid containing all cells.

    Attributes:
        width (int): Number of cells in each row.
        height (int): Number of cells in each column.
        cell_size (int): Size of each cell in pixels.
        grid (list of list of Cell): A 2D list of cells.
        alive_count (int): The current count of alive cells in the grid.
        spawing (bool): Indicates if random spawning of cells is enabled.
    """
    
    def __init__(self, width, height, cell_size):
        """
        Initialize the game grid.

        Args:
            width (int): Number of cells in each row.
            height (int): Number of cells in each column.
            cell_size (int): Size of each cell in pixels.
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[Cell(False) for _ in range(height)] for _ in range(width)]
        self.alive_count = 0
        self.spawing = False

    def draw(self, screen):
        """
        Draw the grid on the Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame display surface.
        """
        for x in range(self.width):
            for y in range(self.height):
                color = "white" if self.grid[x][y].is_alive else "black"
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size
                    ),
                )

    def update(self):
        """
        Update the grid based on the rules of Conway's Game of Life,
        with a chance for dead cells to randomly come alive.
        """
        new_grid = [[Cell(False) for _ in range(self.height)] for _ in range(self.width)]
        new_alive_count = 0
        life_chance = 1

        for x in range(self.width):
            for y in range(self.height):
                rand_num = random.randint(1, life_chance)
                neighbors = self.grid[x][y].check_neighbors(self.grid, x, y)
                if self.grid[x][y].is_alive:
                    new_grid[x][y].is_alive = neighbors in [2, 3]
                else:
                    new_grid[x][y].is_alive = neighbors == 3
                    if rand_num == 1 and life_chance < 1000 and self.spawing:
                        self.grid[x][y].is_alive = True
                        life_chance += 1

                if new_grid[x][y].is_alive:
                    new_alive_count += 1

        self.grid = new_grid
        self.alive_count = new_alive_count
