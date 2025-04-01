import pygame

class InventoryUI:
    def __init__(self, config):
        self.config = config
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # UI元素位置
        self.inventory_rect = pygame.Rect(50, 50, 700, 500)
        self.item_slot_size = 60
        self.item_slots = []
        self.selected_slot = None
        
        # 初始化物品槽
        self.init_item_slots()
        
    def init_item_slots(self):
        # 创建5x5的物品槽网格
        for row in range(5):
            for col in range(5):
                x = 70 + col * (self.item_slot_size + 10)
                y = 70 + row * (self.item_slot_size + 10)
                self.item_slots.append(pygame.Rect(x, y, self.item_slot_size, self.item_slot_size))
                
    def render(self, screen, player):
        # 渲染物品栏背景
        self.render_inventory_background(screen)
        
        # 渲染物品栏标题
        title = self.font.render("物品栏", True, (255, 255, 255))
        screen.blit(title, (60, 30))
        
        # 渲染物品槽
        self.render_item_slots(screen, player)
        
        # 渲染选中物品的详细信息
        if self.selected_slot is not None:
            self.render_item_details(screen, player)
            
    def render_inventory_background(self, screen):
        # 创建半透明黑色背景
        overlay = pygame.Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # 渲染物品栏面板
        pygame.draw.rect(screen, (50, 50, 50), self.inventory_rect)
        
    def render_item_slots(self, screen, player):
        # 渲染所有物品槽
        for i, slot_rect in enumerate(self.item_slots):
            # 绘制物品槽背景
            pygame.draw.rect(screen, (70, 70, 70), slot_rect)
            pygame.draw.rect(screen, (100, 100, 100), slot_rect, 2)
            
            # 如果物品槽有物品，渲染物品
            if i < len(player.inventory):
                item = player.inventory[i]
                self.render_item(screen, item, slot_rect)
                
            # 如果物品槽被选中，绘制高亮边框
            if i == self.selected_slot:
                pygame.draw.rect(screen, (255, 255, 0), slot_rect, 3)
                
    def render_item(self, screen, item, slot_rect):
        # 渲染物品图标（这里用文字代替）
        item_text = self.small_font.render(item.name[:2], True, (255, 255, 255))
        text_rect = item_text.get_rect(center=slot_rect.center)
        screen.blit(item_text, text_rect)
        
    def render_item_details(self, screen, player):
        if self.selected_slot is not None and self.selected_slot < len(player.inventory):
            item = player.inventory[self.selected_slot]
            
            # 创建详细信息面板
            details_rect = pygame.Rect(400, 70, 300, 200)
            pygame.draw.rect(screen, (50, 50, 50), details_rect)
            
            # 渲染物品名称
            name_text = self.font.render(item.name, True, (255, 255, 255))
            screen.blit(name_text, (420, 90))
            
            # 渲染物品描述
            desc_text = self.small_font.render(item.description, True, (200, 200, 200))
            screen.blit(desc_text, (420, 130))
            
            # 渲染物品属性
            if hasattr(item, 'damage'):
                damage_text = self.small_font.render(f"伤害: {item.damage}", True, (200, 200, 200))
                screen.blit(damage_text, (420, 160))
            if hasattr(item, 'defense'):
                defense_text = self.small_font.render(f"防御: {item.defense}", True, (200, 200, 200))
                screen.blit(defense_text, (420, 190))
                
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击了物品槽
            for i, slot_rect in enumerate(self.item_slots):
                if slot_rect.collidepoint(event.pos):
                    self.selected_slot = i
                    return "select_item", i
                    
        return None, None 