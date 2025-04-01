import pygame

class TimeSystem:
    def __init__(self, config):
        self.config = config
        self.time = 0  # 游戏内时间（分钟）
        self.day = 1
        self.season = "spring"  # spring, summer, autumn, winter
        self.time_scale = 1.0  # 时间流逝速度
        self.load_time_images()
        
    def load_time_images(self):
        # 加载时间相关的图片
        self.time_images = {
            "sun": pygame.Surface((100, 100)),
            "moon": pygame.Surface((100, 100)),
            "stars": pygame.Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        }
        
        # 设置太阳颜色
        pygame.draw.circle(self.time_images["sun"], (255, 255, 0), (50, 50), 40)
        
        # 设置月亮颜色
        pygame.draw.circle(self.time_images["moon"], (200, 200, 255), (50, 50), 40)
        
        # 设置星空
        for _ in range(100):
            x = random.randint(0, self.config.WINDOW_WIDTH)
            y = random.randint(0, self.config.WINDOW_HEIGHT)
            pygame.draw.circle(self.time_images["stars"], (255, 255, 255),
                             (x, y), 1)
                             
    def update(self, delta_time):
        # 更新时间
        self.time += delta_time * self.time_scale
        
        # 检查是否需要更新日期
        if self.time >= 1440:  # 1440分钟 = 24小时
            self.time -= 1440
            self.day += 1
            
            # 检查是否需要更新季节
            if self.day > 90:  # 每90天换季
                self.day = 1
                self.update_season()
                
    def update_season(self):
        seasons = ["spring", "summer", "autumn", "winter"]
        current_index = seasons.index(self.season)
        self.season = seasons[(current_index + 1) % 4]
        
    def get_time_of_day(self):
        # 返回当前时间段
        hour = int(self.time / 60)
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
            
    def get_light_level(self):
        # 返回当前光照等级（0-1）
        hour = self.time / 60
        if 5 <= hour < 7:  # 日出
            return (hour - 5) / 2
        elif 7 <= hour < 17:  # 白天
            return 1.0
        elif 17 <= hour < 19:  # 日落
            return (19 - hour) / 2
        else:  # 夜晚
            return 0.2
            
    def render(self, screen):
        # 渲染时间效果
        light_level = self.get_light_level()
        
        # 创建光照遮罩
        overlay = pygame.Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(int(255 * (1 - light_level)))
        screen.blit(overlay, (0, 0))
        
        # 渲染太阳/月亮
        time_of_day = self.get_time_of_day()
        if time_of_day in ["morning", "afternoon"]:
            screen.blit(self.time_images["sun"], (50, 50))
        elif time_of_day == "night":
            screen.blit(self.time_images["stars"], (0, 0))
            screen.blit(self.time_images["moon"], (50, 50))
            
    def get_time_effects(self):
        # 返回时间对游戏的影响
        effects = {
            "visibility": 1.0,
            "combat_accuracy": 1.0,
            "stealth_bonus": 0.0
        }
        
        time_of_day = self.get_time_of_day()
        if time_of_day == "night":
            effects["visibility"] = 0.4
            effects["combat_accuracy"] = 0.8
            effects["stealth_bonus"] = 0.3
        elif time_of_day in ["morning", "evening"]:
            effects["visibility"] = 0.7
            effects["combat_accuracy"] = 0.9
            
        return effects
        
    def get_season_effects(self):
        # 返回季节对游戏的影响
        effects = {
            "temperature": 20,
            "movement_speed": 1.0,
            "resource_availability": 1.0
        }
        
        if self.season == "spring":
            effects["temperature"] = 15
            effects["resource_availability"] = 1.2
        elif self.season == "summer":
            effects["temperature"] = 30
            effects["movement_speed"] = 0.9
        elif self.season == "autumn":
            effects["temperature"] = 15
            effects["resource_availability"] = 1.1
        elif self.season == "winter":
            effects["temperature"] = 0
            effects["movement_speed"] = 0.8
            effects["resource_availability"] = 0.7
            
        return effects 