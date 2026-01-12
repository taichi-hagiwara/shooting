import pygame
from pygame.math import Vector2
from constants import RED, CELL_SIZE, GRID_SIZE

class Enemy:
    def __init__(self, spawn_pos, target_pos, speed):
        self.pos = spawn_pos  # 現在位置 (Vector2)
        self.target = target_pos  # 目標地点 (Vector2)
        self.speed = speed  # 移動速度 (px/フレーム)
        self.active = True  # 活動中フラグ

        # 対象への移動方向ベクトルを計算
        self.direction = (self.target - self.pos).normalize()

    def update(self, grid):
        if not self.active:
            return  # 非アクティブの場合何もしない

        # 目標地点へ移動
        self.pos += self.direction * self.speed

        # 現在のマス座標を計算
        grid_pos = Vector2(int(self.pos.x // CELL_SIZE), int(self.pos.y // CELL_SIZE))

        # マス内に到達した場合の処理
        if grid_pos == self.target:
            grid.set_tile_black(int(grid_pos.x), int(grid_pos.y))  # そのマスを黒に変更
            self.active = False  # 非アクティブにする

    def draw(self, screen):
        """
        敵を画面に描画
        """
        if self.active:
            pygame.draw.rect(
                screen, RED,
                (self.pos.x, self.pos.y, CELL_SIZE, CELL_SIZE)  # px単位の位置で描画
            )