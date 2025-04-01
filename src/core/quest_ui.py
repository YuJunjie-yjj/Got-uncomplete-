import pygame

class QuestUI:
    def __init__(self, config):
        self.config = config
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # UI元素位置
        self.quest_log_rect = pygame.Rect(50, 50, 700, 500)
        self.quest_list_rect = pygame.Rect(70, 100, 300, 400)
        self.quest_details_rect = pygame.Rect(400, 100, 300, 400)
        self.selected_quest = None
        
    def render(self, screen, story_manager):
        # 渲染任务日志背景
        self.render_quest_log_background(screen)
        
        # 渲染任务日志标题
        title = self.font.render("任务日志", True, (255, 255, 255))
        screen.blit(title, (60, 30))
        
        # 渲染任务列表
        self.render_quest_list(screen, story_manager)
        
        # 渲染选中任务的详细信息
        if self.selected_quest:
            self.render_quest_details(screen, story_manager)
            
    def render_quest_log_background(self, screen):
        # 创建半透明黑色背景
        overlay = pygame.Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # 渲染任务日志面板
        pygame.draw.rect(screen, (50, 50, 50), self.quest_log_rect)
        
    def render_quest_list(self, screen, story_manager):
        # 渲染任务列表背景
        pygame.draw.rect(screen, (70, 70, 70), self.quest_list_rect)
        
        # 渲染活动任务
        active_title = self.small_font.render("进行中的任务", True, (255, 255, 255))
        screen.blit(active_title, (80, 110))
        
        y_pos = 140
        for quest in story_manager.active_quests:
            # 渲染任务名称
            quest_text = self.small_font.render(quest["name"], True, (200, 200, 200))
            screen.blit(quest_text, (90, y_pos))
            
            # 如果任务被选中，绘制高亮背景
            if quest == self.selected_quest:
                pygame.draw.rect(screen, (100, 100, 100),
                               (85, y_pos - 5, 280, 25))
                
            y_pos += 30
            
        # 渲染已完成任务
        completed_title = self.small_font.render("已完成的任务", True, (255, 255, 255))
        screen.blit(completed_title, (80, y_pos + 10))
        
        y_pos += 40
        for quest in story_manager.completed_quests:
            # 渲染任务名称（灰色）
            quest_text = self.small_font.render(quest["name"], True, (100, 100, 100))
            screen.blit(quest_text, (90, y_pos))
            y_pos += 30
            
    def render_quest_details(self, screen, story_manager):
        if self.selected_quest:
            # 渲染任务详情背景
            pygame.draw.rect(screen, (70, 70, 70), self.quest_details_rect)
            
            # 渲染任务名称
            name_text = self.font.render(self.selected_quest["name"], True, (255, 255, 255))
            screen.blit(name_text, (420, 120))
            
            # 渲染任务描述
            desc_text = self.small_font.render(self.selected_quest["description"], True, (200, 200, 200))
            screen.blit(desc_text, (420, 160))
            
            # 渲染任务目标
            objectives_title = self.small_font.render("任务目标:", True, (255, 255, 255))
            screen.blit(objectives_title, (420, 200))
            
            y_pos = 230
            for objective in self.selected_quest["objectives"]:
                # 根据目标完成状态选择颜色
                color = (0, 255, 0) if objective["completed"] else (200, 200, 200)
                objective_text = self.small_font.render(
                    f"- {objective['description']}",
                    True, color
                )
                screen.blit(objective_text, (420, y_pos))
                y_pos += 30
                
            # 渲染任务奖励
            rewards_title = self.small_font.render("任务奖励:", True, (255, 255, 255))
            screen.blit(rewards_title, (420, y_pos + 10))
            
            y_pos += 40
            for reward in self.selected_quest["rewards"]:
                reward_text = self.small_font.render(
                    f"- {reward['type']}: {reward['amount']}",
                    True, (200, 200, 200)
                )
                screen.blit(reward_text, (420, y_pos))
                y_pos += 30
                
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击了任务列表
            if self.quest_list_rect.collidepoint(event.pos):
                # 计算点击的任务索引
                y_pos = event.pos[1] - 140
                quest_index = y_pos // 30
                
                # 检查是否点击了活动任务
                if 0 <= quest_index < len(self.story_manager.active_quests):
                    self.selected_quest = self.story_manager.active_quests[quest_index]
                    return "select_quest", self.selected_quest
                    
        return None, None 