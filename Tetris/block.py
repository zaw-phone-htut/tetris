from colors import Colors
from position import Position
import pygame


class Block:

    def __init__(self, id):
        self.id = id  # Id will take int value for colors
        self.cells = {}  # Child will have rotational positions in here as dict
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.color = Colors.get_cell_colors()

    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_position()
        for tile in tiles:
            if tile.row >= 0:
                tile_rect = pygame.Rect(tile.column * self.cell_size + offset_x, tile.row *
                                        self.cell_size + offset_y, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.color[self.id], tile_rect)

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotate(self):
        self.rotation_state -= 1
        if self.rotation_state < 0:
            self.rotation_state = len(self.cells) - 1

    def get_cell_position(self):
        tiles = self.cells[self.rotation_state]  # Get the current position
        moved_tile = []
        for position in tiles:
            # Assign Updated/Moved Position to "position" variable
            position = Position(position.row + self.row_offset,
                                position.column + self.column_offset)
            moved_tile.append(position)
        return moved_tile
