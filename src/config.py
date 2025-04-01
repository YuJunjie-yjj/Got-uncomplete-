class Config:
    def __init__(self):
        # 窗口设置
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.WINDOW_TITLE = "权力的游戏"
        self.FPS = 60
        
        # 游戏设置
        self.TILE_SIZE = 32
        self.PLAYER_SPEED = 5
        self.CAMERA_SMOOTH_SPEED = 0.1
        
        # 战斗设置
        self.COMBAT_TURN_TIME = 1.0
        self.COMBAT_ANIMATION_SPEED = 0.5
        
        # 对话设置
        self.DIALOGUE_TEXT_SPEED = 0.05
        self.DIALOGUE_CHOICE_SPACING = 40
        
        # 物品栏设置
        self.INVENTORY_SLOT_SIZE = 60
        self.INVENTORY_GRID_SIZE = 5
        
        # 技能树设置
        self.SKILL_POINT_COST = 1
        self.SKILL_LEVEL_REQUIREMENT = 5
        
        # 天气设置
        self.WEATHER_CHANGE_INTERVAL = 300  # 5分钟
        self.WEATHER_EFFECT_INTENSITY = 0.5
        
        # 时间设置
        self.TIME_SCALE = 1.0  # 1秒 = 1分钟
        self.DAY_LENGTH = 1440  # 24小时 = 1440分钟
        self.SEASON_LENGTH = 90  # 90天
        
        # 音频设置
        self.MUSIC_VOLUME = 0.5
        self.SOUND_VOLUME = 0.7
        
        # 存档设置
        self.SAVE_SLOTS = 5
        self.AUTO_SAVE_INTERVAL = 300  # 5分钟
        
        # 调试设置
        self.DEBUG_MODE = False
        self.SHOW_COLLISION = False
        self.SHOW_FPS = False
        self.SHOW_GRID = False 