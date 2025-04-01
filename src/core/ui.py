import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 36)
        self.is_hovered = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.current_color = self.hover_color if self.is_hovered else self.color
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False
        
    def render(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Menu:
    def __init__(self, config):
        self.config = config
        self.buttons = []
        self.background = None
        self.title_font = pygame.font.Font(None, 74)
        self.title_text = "权力的游戏：维斯特洛的传说"
        
    def init_main_menu(self):
        # 创建主菜单按钮
        button_width = 200
        button_height = 50
        start_x = self.config.WINDOW_WIDTH // 2 - button_width // 2
        start_y = self.config.WINDOW_HEIGHT // 2
        
        self.buttons = [
            Button(start_x, start_y, button_width, button_height, 
                  "开始游戏", (100, 100, 100), (150, 150, 150)),
            Button(start_x, start_y + 70, button_width, button_height,
                  "选择角色", (100, 100, 100), (150, 150, 150)),
            Button(start_x, start_y + 140, button_width, button_height,
                  "设置", (100, 100, 100), (150, 150, 150)),
            Button(start_x, start_y + 210, button_width, button_height,
                  "退出", (100, 100, 100), (150, 150, 150))
        ]
        
    def init_character_select(self):
        # 创建角色选择菜单按钮
        button_width = 300
        button_height = 60
        start_x = self.config.WINDOW_WIDTH // 2 - button_width // 2
        start_y = 200
        
        characters = [
            ("琼恩·雪诺", "守夜人新兵"),
            ("丹妮莉丝·坦格利安", "龙之母"),
            ("提利昂·兰尼斯特", "小恶魔"),
            ("艾莉亚·史塔克", "无面者")
        ]
        
        self.buttons = []
        for i, (name, title) in enumerate(characters):
            self.buttons.append(
                Button(start_x, start_y + i * 80, button_width, button_height,
                      f"{name} - {title}", (100, 100, 100), (150, 150, 150))
            )
            
        # 添加返回按钮
        self.buttons.append(
            Button(start_x, start_y + len(characters) * 80 + 40,
                  button_width, button_height, "返回", (100, 100, 100), (150, 150, 150))
        )
        
    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                if button.handle_event(event):
                    return button.text
        return None
        
    def render(self, screen):
        # 渲染背景
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((0, 0, 0))
            
        # 渲染标题
        title_surface = self.title_font.render(self.title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.config.WINDOW_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # 渲染按钮
        for button in self.buttons:
            button.render(screen) 