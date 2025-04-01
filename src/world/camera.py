import pygame

class Camera:
    def __init__(self, config):
        self.config = config
        self.x = 0
        self.y = 0
        self.target = None
        self.smooth_speed = 0.1
        
    def set_target(self, target):
        self.target = target
        
    def update(self):
        if self.target:
            # 计算目标位置（使目标位于屏幕中心）
            target_x = self.target.x - self.config.WINDOW_WIDTH // 2
            target_y = self.target.y - self.config.WINDOW_HEIGHT // 2
            
            # 平滑移动相机
            self.x += (target_x - self.x) * self.smooth_speed
            self.y += (target_y - self.y) * self.smooth_speed
            
    def apply(self, entity):
        # 将世界坐标转换为屏幕坐标
        return entity.x - self.x, entity.y - self.y
        
    def apply_rect(self, rect):
        # 将世界矩形转换为屏幕矩形
        return pygame.Rect(rect.x - self.x, rect.y - self.y,
                         rect.width, rect.height)
        
    def reverse_apply(self, screen_x, screen_y):
        # 将屏幕坐标转换为世界坐标
        return screen_x + self.x, screen_y + self.y
        
    def reverse_apply_rect(self, screen_rect):
        # 将屏幕矩形转换为世界矩形
        return pygame.Rect(screen_rect.x + self.x, screen_rect.y + self.y,
                         screen_rect.width, screen_rect.height) 