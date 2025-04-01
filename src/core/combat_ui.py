import pygame

class CombatUI:
    def __init__(self, config):
        self.config = config
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # UI元素位置
        self.action_menu_rect = pygame.Rect(50, 400, 700, 200)
        self.target_menu_rect = pygame.Rect(50, 200, 700, 150)
        self.status_rect = pygame.Rect(50, 50, 700, 100)
        
        # 战斗状态
        self.selected_action = None
        self.selected_target = None
        self.show_target_menu = False
        
    def render(self, screen, combat_system, player):
        # 渲染战斗背景
        self.render_combat_background(screen)
        
        # 渲染状态栏
        self.render_status_bar(screen, player)
        
        # 渲染战斗者信息
        self.render_combatants(screen, combat_system)
        
        # 渲染动作菜单
        self.render_action_menu(screen, combat_system)
        
        # 如果选择了动作，显示目标选择菜单
        if self.show_target_menu:
            self.render_target_menu(screen, combat_system)
            
    def render_combat_background(self, screen):
        # 创建半透明黑色背景
        overlay = pygame.Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
    def render_status_bar(self, screen, player):
        # 渲染玩家状态
        health_text = f"生命值: {player.health}/{player.max_health}"
        health_surface = self.font.render(health_text, True, (255, 255, 255))
        screen.blit(health_surface, (60, 60))
        
        # 渲染生命值条
        health_bar_width = 200
        health_bar_height = 20
        health_percentage = player.health / player.max_health
        
        # 背景条
        pygame.draw.rect(screen, (100, 100, 100),
                        (60, 90, health_bar_width, health_bar_height))
        # 生命值条
        pygame.draw.rect(screen, (255, 0, 0),
                        (60, 90, health_bar_width * health_percentage, health_bar_height))
        
    def render_combatants(self, screen, combat_system):
        # 渲染所有战斗者的状态
        for i, combatant in enumerate(combat_system.combatants):
            y_pos = 150 + i * 40
            name_text = f"{combatant.name} - 生命值: {combatant.health}/{combatant.max_health}"
            name_surface = self.small_font.render(name_text, True, (255, 255, 255))
            screen.blit(name_surface, (60, y_pos))
            
            # 如果是当前回合的战斗者，显示高亮
            if i == combat_system.current_turn:
                pygame.draw.rect(screen, (255, 255, 0),
                               (55, y_pos - 5, 710, 30), 2)
                
    def render_action_menu(self, screen, combat_system):
        # 渲染动作菜单背景
        pygame.draw.rect(screen, (50, 50, 50), self.action_menu_rect)
        
        # 渲染可用动作
        current_combatant = combat_system.combatants[combat_system.current_turn]
        if current_combatant == self.player:
            actions = ["攻击", "防御", "使用物品", "逃跑"]
            for i, action in enumerate(actions):
                action_text = self.small_font.render(action, True, (255, 255, 255))
                screen.blit(action_text, (70, 420 + i * 40))
                
    def render_target_menu(self, screen, combat_system):
        # 渲染目标菜单背景
        pygame.draw.rect(screen, (50, 50, 50), self.target_menu_rect)
        
        # 渲染可选目标
        for i, target in enumerate(combat_system.combatants):
            if target != self.player and not target.is_dead:
                target_text = self.small_font.render(
                    f"{target.name} - 生命值: {target.health}/{target.max_health}",
                    True, (255, 255, 255)
                )
                screen.blit(target_text, (70, 220 + i * 30))
                
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击了动作菜单
            if self.action_menu_rect.collidepoint(event.pos):
                y_pos = event.pos[1] - 420
                action_index = y_pos // 40
                if 0 <= action_index < 4:  # 4个动作选项
                    self.selected_action = ["attack", "defend", "use_item", "flee"][action_index]
                    self.show_target_menu = True
                    
            # 检查是否点击了目标菜单
            elif self.show_target_menu and self.target_menu_rect.collidepoint(event.pos):
                y_pos = event.pos[1] - 220
                target_index = y_pos // 30
                if 0 <= target_index < len(self.combat_system.combatants):
                    self.selected_target = self.combat_system.combatants[target_index]
                    return self.selected_action, self.selected_target
                    
        return None, None 