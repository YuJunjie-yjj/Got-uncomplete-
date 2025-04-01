import pygame
import os
import json

class ResourceManager:
    def __init__(self, config):
        self.config = config
        self.images = {}
        self.animations = {}
        self.fonts = {}
        self.load_resources()
        
    def load_resources(self):
        # 加载图片资源
        self.load_images()
        
        # 加载动画资源
        self.load_animations()
        
        # 加载字体资源
        self.load_fonts()
        
    def load_images(self):
        # 加载角色图片
        characters_dir = "assets/images/characters"
        for filename in os.listdir(characters_dir):
            if filename.endswith('.png'):
                image_name = os.path.splitext(filename)[0]
                image_path = os.path.join(characters_dir, filename)
                self.images[image_name] = pygame.image.load(image_path).convert_alpha()
                
        # 加载物品图片
        items_dir = "assets/images/items"
        for filename in os.listdir(items_dir):
            if filename.endswith('.png'):
                image_name = os.path.splitext(filename)[0]
                image_path = os.path.join(items_dir, filename)
                self.images[image_name] = pygame.image.load(image_path).convert_alpha()
                
        # 加载UI图片
        ui_dir = "assets/images/ui"
        for filename in os.listdir(ui_dir):
            if filename.endswith('.png'):
                image_name = os.path.splitext(filename)[0]
                image_path = os.path.join(ui_dir, filename)
                self.images[image_name] = pygame.image.load(image_path).convert_alpha()
                
        # 加载环境图片
        environment_dir = "assets/images/environment"
        for filename in os.listdir(environment_dir):
            if filename.endswith('.png'):
                image_name = os.path.splitext(filename)[0]
                image_path = os.path.join(environment_dir, filename)
                self.images[image_name] = pygame.image.load(image_path).convert_alpha()
                
    def load_animations(self):
        # 加载动画数据
        animations_dir = "assets/animations"
        for filename in os.listdir(animations_dir):
            if filename.endswith('.json'):
                animation_name = os.path.splitext(filename)[0]
                animation_path = os.path.join(animations_dir, filename)
                
                with open(animation_path, 'r', encoding='utf-8') as f:
                    animation_data = json.load(f)
                    
                # 创建动画序列
                animation = {
                    "frames": [],
                    "frame_duration": animation_data["frame_duration"],
                    "loop": animation_data.get("loop", True)
                }
                
                # 加载动画帧
                for frame_data in animation_data["frames"]:
                    frame_image = self.images[frame_data["image"]]
                    frame_rect = pygame.Rect(
                        frame_data["x"],
                        frame_data["y"],
                        frame_data["width"],
                        frame_data["height"]
                    )
                    animation["frames"].append((frame_image, frame_rect))
                    
                self.animations[animation_name] = animation
                
    def load_fonts(self):
        # 加载字体文件
        fonts_dir = "assets/fonts"
        for filename in os.listdir(fonts_dir):
            if filename.endswith('.ttf'):
                font_name = os.path.splitext(filename)[0]
                font_path = os.path.join(fonts_dir, filename)
                
                # 创建不同大小的字体
                self.fonts[font_name] = {
                    "small": pygame.font.Font(font_path, 16),
                    "medium": pygame.font.Font(font_path, 24),
                    "large": pygame.font.Font(font_path, 32)
                }
                
    def get_image(self, image_name):
        return self.images.get(image_name)
        
    def get_animation(self, animation_name):
        return self.animations.get(animation_name)
        
    def get_font(self, font_name, size="medium"):
        if font_name in self.fonts and size in self.fonts[font_name]:
            return self.fonts[font_name][size]
        return None
        
    def scale_image(self, image, scale):
        if isinstance(image, pygame.Surface):
            new_size = (int(image.get_width() * scale),
                       int(image.get_height() * scale))
            return pygame.transform.scale(image, new_size)
        return image
        
    def rotate_image(self, image, angle):
        if isinstance(image, pygame.Surface):
            return pygame.transform.rotate(image, angle)
        return image
        
    def create_text_surface(self, text, font_name, size="medium", color=(255, 255, 255)):
        font = self.get_font(font_name, size)
        if font:
            return font.render(text, True, color)
        return None
        
    def create_button(self, text, font_name, size="medium", color=(255, 255, 255),
                     hover_color=(200, 200, 200)):
        # 创建按钮背景
        text_surface = self.create_text_surface(text, font_name, size, color)
        if not text_surface:
            return None
            
        # 创建按钮表面
        padding = 10
        button_surface = pygame.Surface((
            text_surface.get_width() + padding * 2,
            text_surface.get_height() + padding * 2
        ))
        button_surface.fill((50, 50, 50))
        
        # 添加文本
        text_rect = text_surface.get_rect(center=button_surface.get_rect().center)
        button_surface.blit(text_surface, text_rect)
        
        return button_surface 