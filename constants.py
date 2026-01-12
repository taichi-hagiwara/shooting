# 画面設定
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE

# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# ゲーム設定
FPS = 60
BULLET_RECHARGE_TIME = 3 * FPS  # 3秒に1発補充
GAME_TIME = 60 * FPS            # 1分間生存が目標
MAX_BULLETS = 10               # 最大装填数