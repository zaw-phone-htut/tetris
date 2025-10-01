from grid import Grid
from props import *
import random
import pygame


class Game:

    def __init__(self):
        self.grid = Grid()
        self.blocks = [J_Block(), L_Block(), S_Block(), Z_Block(),
                       Square_Block(), Line_Block(), T_Block()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.level = 0
        self.lines_cleared_total = 0
        self.clear_sound = pygame.mixer.Sound("audio/line_clear.ogg")
        self.tetris_sound = pygame.mixer.Sound("audio/tetris.ogg")
        self.clear_sound.set_volume(0.5)
        self.tetris_sound.set_volume(0.5)

        pygame.mixer.music.load("audio/music.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def update_score(self, lines_cleared):
        # Classic Tetris scoring
        scoring = {1: 40, 2: 100, 3: 300, 4: 1200}
        if lines_cleared in scoring:
            self.score += scoring[lines_cleared] * (self.level + 1)
        self.lines_cleared_total += lines_cleared
        # Level up every 10 lines
        self.level = self.lines_cleared_total // 10

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [J_Block(), L_Block(), S_Block(), Z_Block(),
                           Square_Block(), Line_Block(), T_Block()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def hard_drop(self):
        ghost_positions = self.get_ghost_block_positions()
        # Find the max row offset for the ghost block
        max_row = max(tile.row for tile in ghost_positions)
        # Calculate how far to move down
        drop_distance = max_row - \
            max(tile.row for tile in self.current_block.get_cell_position())
        self.current_block.move(drop_distance, 0)
        self.lock_block()

    def get_ghost_block_positions(self):
        # Create a copy of the current block
        ghost_block = type(self.current_block)()
        ghost_block.rotation_state = self.current_block.rotation_state
        ghost_block.row_offset = self.current_block.row_offset
        ghost_block.column_offset = self.current_block.column_offset

        # Move the ghost block down until it collides
        while True:
            ghost_block.move(1, 0)
            if not self.is_block_inside_block(ghost_block) or not self.is_fit_block(ghost_block):
                ghost_block.move(-1, 0)
                break
        return ghost_block.get_cell_position()

    def is_block_inside_block(self, block):
        tiles = block.get_cell_position()
        for tile in tiles:
            # Ignore top border (row < 0 is allowed)
            if tile.column < 0 or tile.column >= self.grid.num_columns:
                return False
            if tile.row >= self.grid.num_rows:
                return False
        return True

    def is_fit_block(self, block):
        tiles = block.get_cell_position()
        for tile in tiles:
            # Only check for collision if inside the grid
            if tile.row >= 0 and tile.row < self.grid.num_rows and tile.column >= 0 and tile.column < self.grid.num_columns:
                if not self.grid.is_empty(tile.row, tile.column):
                    return False
        return True

    def reset(self):
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        self.grid.reset()
        self.score = 0
        self.level = 0
        self.lines_cleared_total = 0
        self.blocks = [J_Block(), L_Block(), S_Block(), Z_Block(),
                       Square_Block(), Line_Block(), T_Block()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()

    def is_block_inside(self):
        tiles = self.current_block.get_cell_position()
        for tile in tiles:
            # Ignore top border (row < 0 is allowed)
            if tile.column < 0 or tile.column >= self.grid.num_columns:
                return False
            if tile.row >= self.grid.num_rows:
                return False
        return True

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.is_block_inside() or not self.is_fit():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.is_block_inside() or not self.is_fit():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.is_block_inside() or not self.is_fit():
            self.current_block.move(-1, 0)
            self.lock_block()

    def is_fit(self):
        tiles = self.current_block.get_cell_position()
        for tile in tiles:
            # Only check for collision if inside the grid
            if tile.row >= 0 and tile.row < self.grid.num_rows and tile.column >= 0 and tile.column < self.grid.num_columns:
                if not self.grid.is_empty(tile.row, tile.column):
                    return False
        return True

    def lock_block(self):
        tiles = self.current_block.get_cell_position()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleard = self.grid.clear_full_row()
        if rows_cleard > 0 and rows_cleard <= 3:
            self.clear_sound.play()
            self.update_score(rows_cleard)
        elif rows_cleard >= 4:
            self.tetris_sound.play()
            self.update_score(rows_cleard)
        if not self.is_fit():
            self.game_over = True
            pygame.mixer.music.stop()

    def rotate(self):
        self.current_block.rotate()
        if not self.is_block_inside() or not self.is_fit():
            self.current_block.undo_rotate()

    def draw(self, screen):
        self.grid.draw(screen)
        # Draw ghost block
        ghost_positions = self.get_ghost_block_positions()
        ghost_color = (200, 200, 200)  # Light gray for ghost
        for tile in ghost_positions:
            if tile.row >= 0:
                rect = pygame.Rect(tile.column * self.current_block.cell_size + 11,
                                   tile.row * self.current_block.cell_size + 11,
                                   self.current_block.cell_size - 1,
                                   self.current_block.cell_size - 1)
                pygame.draw.rect(screen, ghost_color, rect, 2)  # Outline only
        self.current_block.draw(screen, 11, 11)
        self.next_block.draw(screen, 240, 270)
