import pygame
import pytmx
import pyscroll

class World:
    def __init__(self, config):
        self.config = config
        self.map_data = None
        self.map_layer = None
        self.camera = None
        
        # 世界状态
        self.time_of_day = 0  # 0-24小时
        self.weather = "clear"  # clear, rain, snow, storm
        self.season = "summer"  # summer, autumn, winter, spring
        
        # 加载地图
        self.load_map("westeros")
        
    def load_map(self, map_name):
        # 加载TMX地图文件
        self.map_data = pytmx.load_pygame(f"{self.config.ASSETS_PATH}/maps/{map_name}.tmx")
        
        # 创建地图层
        map_layer = pyscroll.TiledMapData(self.map_data)
        self.map_layer = pyscroll.BufferedRenderer(map_layer, 
                                                 (self.config.WINDOW_WIDTH, 
                                                  self.config.WINDOW_HEIGHT))
        
        # 创建相机
        self.camera = pyscroll.camera.Camera(self.map_layer)
        
    def update(self):
        # 更新时间
        self.time_of_day = (self.time_of_day + 0.1) % 24
        
        # 更新天气
        self.update_weather()
        
        # 更新季节
        self.update_season()
        
        # 更新相机
        self.camera.update()
        
    def render(self, screen):
        # 渲染地图
        self.map_layer.draw(screen, self.camera)
        
        # 渲染天气效果
        self.render_weather(screen)
        
    def update_weather(self):
        # 简单的天气变化系统
        if pygame.random.random() < 0.001:  # 0.1%的概率改变天气
            weathers = ["clear", "rain", "snow", "storm"]
            self.weather = pygame.random.choice(weathers)
            
    def update_season(self):
        # 每30天改变一次季节
        if self.time_of_day == 0 and pygame.random.random() < 0.01:
            seasons = ["summer", "autumn", "winter", "spring"]
            current_index = seasons.index(self.season)
            self.season = seasons[(current_index + 1) % 4]
            
    def render_weather(self, screen):
        # TODO: 实现天气效果渲染
        pass
        
    def get_tile_at(self, x, y):
        # 获取指定坐标的瓦片
        return self.map_data.get_tile_gid(x, y, 0)
        
    def is_walkable(self, x, y):
        # 检查指定坐标是否可通行
        tile_gid = self.get_tile_at(x, y)
        return tile_gid in self.map_data.properties.get("walkable", [])
        
    def get_region_at(self, x, y):
        # 获取指定坐标所在的区域
        # TODO: 实现区域检测
        return "unknown"
        
    def get_climate_at(self, x, y):
        # 获取指定坐标的气候
        region = self.get_region_at(x, y)
        climates = {
            "north": "cold",
            "riverlands": "temperate",
            "vale": "mountain",
            "westerlands": "temperate",
            "crownlands": "temperate",
            "stormlands": "stormy",
            "reach": "warm",
            "dorne": "desert"
        }
        return climates.get(region, "temperate") 