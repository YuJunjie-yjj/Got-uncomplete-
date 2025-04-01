import pygame
import random
import math

class WeatherSystem:
    def __init__(self, config):
        self.config = config
        self.current_weather = "clear"
        self.weather_duration = 0
        self.weather_intensity = 0.0
        self.particles = []
        self.load_weather_effects()
        
    def load_weather_effects(self):
        # 加载天气效果图片
        self.weather_images = {
            "rain": pygame.Surface((2, 10)),
            "snow": pygame.Surface((4, 4)),
            "fog": pygame.Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        }
        
        # 设置雨滴颜色
        self.weather_images["rain"].fill((200, 200, 255))
        
        # 设置雪花颜色
        self.weather_images["snow"].fill((255, 255, 255))
        
        # 设置雾效果
        self.weather_images["fog"].fill((200, 200, 200))
        self.weather_images["fog"].set_alpha(50)
        
    def update(self, delta_time):
        # 更新天气持续时间
        self.weather_duration -= delta_time
        
        # 如果天气持续时间结束，随机选择新天气
        if self.weather_duration <= 0:
            self.change_weather()
            
        # 更新天气粒子
        self.update_particles(delta_time)
        
    def change_weather(self):
        # 随机选择新天气
        weather_types = ["clear", "rain", "snow", "fog"]
        weights = [0.4, 0.3, 0.2, 0.1]  # 不同天气的出现概率
        
        self.current_weather = random.choices(weather_types, weights=weights)[0]
        self.weather_duration = random.uniform(300, 900)  # 5-15分钟
        self.weather_intensity = random.uniform(0.3, 1.0)
        
        # 根据新天气初始化粒子
        self.init_particles()
        
    def init_particles(self):
        self.particles = []
        num_particles = int(100 * self.weather_intensity)
        
        if self.current_weather == "rain":
            for _ in range(num_particles):
                self.particles.append({
                    "x": random.randint(0, self.config.WINDOW_WIDTH),
                    "y": random.randint(-100, 0),
                    "speed": random.uniform(5, 10),
                    "length": random.uniform(5, 15)
                })
        elif self.current_weather == "snow":
            for _ in range(num_particles):
                self.particles.append({
                    "x": random.randint(0, self.config.WINDOW_WIDTH),
                    "y": random.randint(-50, 0),
                    "speed_x": random.uniform(-1, 1),
                    "speed_y": random.uniform(1, 3),
                    "size": random.uniform(2, 4)
                })
                
    def update_particles(self, delta_time):
        if self.current_weather == "rain":
            for particle in self.particles:
                particle["y"] += particle["speed"]
                if particle["y"] > self.config.WINDOW_HEIGHT:
                    particle["y"] = -100
                    particle["x"] = random.randint(0, self.config.WINDOW_WIDTH)
                    
        elif self.current_weather == "snow":
            for particle in self.particles:
                particle["x"] += particle["speed_x"]
                particle["y"] += particle["speed_y"]
                if (particle["y"] > self.config.WINDOW_HEIGHT or
                    particle["x"] < 0 or
                    particle["x"] > self.config.WINDOW_WIDTH):
                    particle["y"] = -50
                    particle["x"] = random.randint(0, self.config.WINDOW_WIDTH)
                    
    def render(self, screen):
        if self.current_weather == "clear":
            return
            
        # 渲染天气效果
        if self.current_weather == "rain":
            for particle in self.particles:
                pygame.draw.line(screen, (200, 200, 255),
                               (particle["x"], particle["y"]),
                               (particle["x"], particle["y"] + particle["length"]))
                               
        elif self.current_weather == "snow":
            for particle in self.particles:
                pygame.draw.circle(screen, (255, 255, 255),
                                 (int(particle["x"]), int(particle["y"])),
                                 int(particle["size"]))
                                 
        elif self.current_weather == "fog":
            screen.blit(self.weather_images["fog"], (0, 0))
            
    def get_weather_effects(self):
        # 返回当前天气对游戏的影响
        effects = {
            "visibility": 1.0,
            "movement_speed": 1.0,
            "combat_accuracy": 1.0
        }
        
        if self.current_weather == "rain":
            effects["visibility"] = 0.8
            effects["movement_speed"] = 0.9
            effects["combat_accuracy"] = 0.9
        elif self.current_weather == "snow":
            effects["visibility"] = 0.6
            effects["movement_speed"] = 0.7
            effects["combat_accuracy"] = 0.8
        elif self.current_weather == "fog":
            effects["visibility"] = 0.4
            effects["movement_speed"] = 0.8
            effects["combat_accuracy"] = 0.7
            
        return effects 