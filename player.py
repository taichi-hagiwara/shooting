import pygame
from pygame.math import Vector2
from constants import BLUE, CELL_SIZE, GRID_SIZE

class Player:
  def __init__(self, default_pos):

    self.pos = default_pos  # プレイヤーの現在位置（グリッド座標で管理）

  def move_player(self, dx, dy, grid):
    # プレイヤーの新しい位置を計算
    new_pos = self.pos + Vector2(dx, dy)

    if 0 <= new_pos.x < GRID_SIZE and 0 <= new_pos.y < GRID_SIZE and grid.is_white(new_pos.x, new_pos.y):
      self.pos = new_pos

  def draw(self, screen):
    pygame.draw.circle(screen, BLUE, (self.pos.x * CELL_SIZE + CELL_SIZE //
                       2, self.pos.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
