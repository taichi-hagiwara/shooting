import pygame as pg
from pygame.math import Vector2
from constants import GRAY, CELL_SIZE, GRID_SIZE,MAX_BULLETS

class Bullet:
    # 残弾数の初期化をクラス変数で管理
    max_bullets = MAX_BULLETS  # 最大装填数
    current_bullets = max_bullets  # 現在の残弾数

    def __init__(self, initial_pos, direction, speed):
        self.pos = initial_pos  # 弾の初期位置
        self.direction = direction.normalize()  # 発射方向を正規化
        self.speed = speed  # 弾の速度
        self.active = True  # 弾が有効かどうか

    @classmethod
    def can_fire(cls):
        
        return cls.current_bullets > 0

    @classmethod
    def decrease_bullet_count(cls):
        
        if cls.current_bullets > 0:
            cls.current_bullets -= 1

    @classmethod
    def recharge_bullets(cls):
        
        cls.current_bullets = cls.max_bullets

    def update(self, grid):
        if not self.active:
            return  # 非アクティブなら何もせずに終了

        # 弾を現在の方向に移動させる
        self.pos += self.direction * self.speed

        # マス座標を計算 (グリッドの位置に変換)
        grid_pos = Vector2(int(self.pos.x // CELL_SIZE), int(self.pos.y // CELL_SIZE))

        # マス範囲外に出た場合 or 黒マスに衝突した場合
        if grid_pos.x < 0 or grid_pos.x >= GRID_SIZE or grid_pos.y < 0 or grid_pos.y >= GRID_SIZE:
            self.active = False
        elif grid.is_black(int(grid_pos.x), int(grid_pos.y)):
            grid.set_tile_white(int(grid_pos.x), int(grid_pos.y))
            self.active = False

    def draw(self, screen):
        if self.active:
            pg.draw.circle(
                screen, GRAY,
                (int(self.pos.x), int(self.pos.y)),  # ピクセル単位で現在の位置を描画
                CELL_SIZE // 4  # 弾の大きさ
            )