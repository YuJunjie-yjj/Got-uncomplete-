class Config:
    def __init__(self):
        # 窗口设置
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.WINDOW_TITLE = "权力的游戏：维斯特洛的传说"
        
        # 游戏设置
        self.FPS = 60
        self.DEBUG_MODE = False
        
        # 角色设置
        self.PLAYER_SPEED = 5
        self.PLAYER_HEALTH = 100
        
        # 战斗设置
        self.COMBAT_DAMAGE_MULTIPLIER = 1.0
        self.COMBAT_DEFENSE_MULTIPLIER = 1.0
        
        # 世界设置
        self.WORLD_SCALE = 1.0
        self.DAY_LENGTH = 1200  # 秒
        
        # 资源路径
        self.ASSETS_PATH = "assets"
        self.MODELS_PATH = f"{self.ASSETS_PATH}/models"
        self.TEXTURES_PATH = f"{self.ASSETS_PATH}/textures"
        self.AUDIO_PATH = f"{self.ASSETS_PATH}/audio" 