import pygame
from pygame.math import Vector2
from constants import WHITE, BLACK, GRID_SIZE, CELL_SIZE

class Grid:
    def __init__(self):
        # 辞書でグリッドを管理
        self.grid = {}

        for x in range(GRID_SIZE):
          for y in range(GRID_SIZE):
            if (x + y) % 2 == 0:
              self.grid[Vector2(x, y)] = WHITE
            else:
              self.grid[Vector2(x, y)] = BLACK
    
    def draw(self, screen):
        # 辞書から各タイル情報を描画
        for pos, color in self.grid.items():
            pygame.draw.rect(
                screen, color, (pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

    def set_tile_white(self, x, y):
        # マスを白にする
        self.grid[Vector2(x, y)] = WHITE

    def set_tile_black(self, x, y):
        # マスを黒にする
        self.grid[Vector2(x, y)] = BLACK

    def is_white(self, x, y):
        # 指定したマスが白かどうかを確認
        return self.grid.get(Vector2(x, y)) == WHITE

    def is_black(self, x, y):
        # 指定したマスが黒かどうかを確認
        return self.grid.get(Vector2(x, y)) == BLACK