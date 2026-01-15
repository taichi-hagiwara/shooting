import pygame
from pygame.math import Vector2
from constants import WIDTH, HEIGHT, GRID_SIZE, CELL_SIZE, FPS, SPAWN_EVENT
from grid import Grid
from bullet import Bullet
from enemy import Enemy
from player import Player
import random

# 初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.time.set_timer(SPAWN_EVENT, 1000)  # 敵スポーンイベントを毎秒1回発生

# グリッドと弾のリスト
grid = Grid()  # グリッドクラスのインスタンス
player = Player(Vector2(GRID_SIZE // 2, GRID_SIZE // 2))  # プレイヤーを中央に配置
bullets = []  # 弾（Bullet）オブジェクトを管理するリスト
enemies = []  # 敵オブジェクトを管理するリスト

def reset_game():
  global bullets, enemies, player, grid, game_over
  bullets = []
  enemies = []
  player = Player(Vector2(GRID_SIZE // 2, GRID_SIZE // 2))
  grid = Grid()
  game_over = False

def spawn_enemy():
  # ランダムに出現位置を決定
  spawn_positions = [
      Vector2(0, CELL_SIZE * GRID_SIZE // 2),  # 左中央
      Vector2(CELL_SIZE * GRID_SIZE - CELL_SIZE,
              CELL_SIZE * GRID_SIZE // 2),  # 右中央
      Vector2(CELL_SIZE * GRID_SIZE // 2, 0),  # 上中央
      Vector2(CELL_SIZE * GRID_SIZE // 2, CELL_SIZE *
              GRID_SIZE - CELL_SIZE),  # 下中央
  ]

  spawn_pos = random.choice(spawn_positions)
  target_pos = Vector2(random.randint(0, GRID_SIZE - 1),
                       random.randint(0, GRID_SIZE - 1))
  enemy = Enemy(spawn_pos, target_pos, speed=2)  # 敵を生成
  enemies.append(enemy)

def display_game_over():
  screen.fill((0, 0, 0))  # 背景を黒にする
  font = pygame.font.Font(None, 72)

  text = font.render("Game Over", True, (255, 0, 0))
  screen.blit(text, (WIDTH // 2 - text.get_width() //
              2, HEIGHT // 2 - text.get_height() // 2))

  subtext = font.render("Press R to Restart", True, (255, 255, 255))
  screen.blit(subtext, (WIDTH // 2 - subtext.get_width() //
              2, HEIGHT // 2 - subtext.get_height() // 2 + 50))

  pygame.display.flip()
  pygame.time.delay(3000)  # 3秒間待つ

  # リセット待機ループ
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
          reset_game()
          return

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
      direction_b = None
      direction_p = None
      if event.key == pygame.K_UP:
        direction_b = Vector2(0, -1)  # 上方向
      elif event.key == pygame.K_DOWN:
        direction_b = Vector2(0, 1)  # 下方向
      elif event.key == pygame.K_LEFT:
        direction_b = Vector2(-1, 0)  # 左方向
      elif event.key == pygame.K_RIGHT:
        direction_b = Vector2(1, 0)  # 右方向

      if direction_b and Bullet.can_fire():  # 弾が発射可能か判定
        # 新しい弾を生成
        bullet = Bullet(player.pos * CELL_SIZE + Vector2(CELL_SIZE //
                        2, CELL_SIZE // 2), direction_b, speed=5)
        bullets.append(bullet)  # 弾をリストに追加
        Bullet.decrease_bullet_count()  # 残弾数を1減らす
      elif not Bullet.can_fire():
        print("残弾がありません！")
    # WASDでプレイヤー移動
      if event.key == pygame.K_w:
        player.move_player(0, -1, grid)  # 上方向
      elif event.key == pygame.K_s:
        player.move_player(0, 1, grid)  # 下方向
      elif event.key == pygame.K_a:
        player.move_player(-1, 0, grid)  # 左方向
      elif event.key == pygame.K_d:
        player.move_player(1, 0, grid)  # 右方向
    # 敵スポーンイベントの処理
    if event.type == SPAWN_EVENT:
      if len(enemies) < 5:  # 敵の上限判定
        spawn_enemy()

  # 更新処理: 弾の状態を更新
  Bullet.recharge_bullet()  # プレイヤーの弾補充処理
  for bullet in bullets[:]:
    bullet.update(grid)
    if not bullet.active:
      bullets.remove(bullet)

  # 描画処理: グリッドと弾
  grid.draw(screen)  # グリッドの描画
  for bullet in bullets:
    bullet.draw(screen)
  player.draw(screen)  # プレイヤーの描画

  # 敵を定期的に生成
  # イベントタイマーを使った敵の自動生成

  # 敵の更新と描画
  for enemy in enemies[:]:
    enemy.update(grid)
    enemy_grid_pos = Vector2(int(enemy.pos.x // CELL_SIZE),
                             int(enemy.pos.y // CELL_SIZE))
    player_grid_pos = Vector2(int(player.pos.x), int(player.pos.y))
    if enemy_grid_pos == player_grid_pos:
      game_over = True  # ゲームオーバーフラグ
      running = False  # ゲームループ終了
      break  # ループを抜ける
    if not enemy.active:
      enemies.remove(enemy)  # 非アクティブな敵を削除
    enemy.draw(screen)

  # 画面更新
  pygame.display.flip()
  clock.tick(FPS)

if game_over:
  display_game_over()
pygame.quit()
