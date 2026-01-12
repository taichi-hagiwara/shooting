import pygame
from pygame.math import Vector2
from constants import WIDTH, HEIGHT, GRID_SIZE, CELL_SIZE, FPS
from grid import Grid
from bullet import Bullet
from enemy import Enemy
import random

# 初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# グリッドと弾のリスト
grid = Grid()  # グリッドクラスのインスタンス
bullets = []  # 弾（Bullet）オブジェクトを管理するリスト
enemies = []  # 敵オブジェクトを管理するリスト

# プレイヤーの仮位置
player_pos = Vector2(WIDTH // 2, HEIGHT // 2)

def spawn_enemy():
    # ランダムに出現位置を決定
    spawn_positions = [
        Vector2(0, CELL_SIZE * GRID_SIZE // 2),  # 左中央
        Vector2(CELL_SIZE * GRID_SIZE - CELL_SIZE, CELL_SIZE * GRID_SIZE // 2),  # 右中央
        Vector2(CELL_SIZE * GRID_SIZE // 2, 0),  # 上中央
        Vector2(CELL_SIZE * GRID_SIZE // 2, CELL_SIZE * GRID_SIZE - CELL_SIZE),  # 下中央
    ]
    
    spawn_pos = random.choice(spawn_positions)
    target_pos = Vector2(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    enemy = Enemy(spawn_pos, target_pos, speed=2)  # 敵を生成
    enemies.append(enemy)

# ゲームループ
running = True
while running:
    screen.fill((0, 0, 0))  # 背景を塗りつぶす

    # イベント処理（入力判定）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 矢印キーで弾を発射
        if event.type == pygame.KEYDOWN:
            direction = None
            if event.key == pygame.K_UP:
                direction = Vector2(0, -1)  # 上方向
            elif event.key == pygame.K_DOWN:
                direction = Vector2(0, 1)  # 下方向
            elif event.key == pygame.K_LEFT:
                direction = Vector2(-1, 0)  # 左方向
            elif event.key == pygame.K_RIGHT:
                direction = Vector2(1, 0)  # 右方向

            if direction and Bullet.can_fire():  # 弾が発射可能か判定
                bullet = Bullet(player_pos, direction, speed=5)  # 新しい弾を生成
                bullets.append(bullet)  # 弾をリストに追加
                Bullet.decrease_bullet_count()  # 残弾数を1減らす
            elif not Bullet.can_fire():
                print("残弾がありません！")

    # 更新処理: 弾の状態を更新
    for bullet in bullets[:]:
        bullet.update(grid)
        if not bullet.active:
            bullets.remove(bullet)

    # 描画処理: グリッドと弾
    grid.draw(screen)  # グリッドの描画
    for bullet in bullets:
        bullet.draw(screen)

    # プレイヤーの位置を描画
    pygame.draw.rect(screen, (0, 0, 255), (player_pos.x, player_pos.y, CELL_SIZE, CELL_SIZE))

    # 敵を定期的に生成
    if len(enemies) < 5:  # 同時に存在できる敵の数を制限
        spawn_enemy()

    # 敵の更新と描画
    for enemy in enemies[:]:
        enemy.update(grid)
        if not enemy.active:
            enemies.remove(enemy)  # 非アクティブな敵を削除
        enemy.draw(screen)

    # 画面更新
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()