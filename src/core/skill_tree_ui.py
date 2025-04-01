import pygame

class SkillTreeUI:
    def __init__(self, config):
        self.config = config
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # UI元素位置
        self.skill_tree_rect = pygame.Rect(50, 50, 700, 500)
        self.skill_radius = 30
        self.skill_positions = {}
        self.selected_skill = None
        
        # 初始化技能位置
        self.init_skill_positions()
        
    def init_skill_positions(self):
        # 定义技能树布局
        self.skill_positions = {
            "combat": {
                "sword_mastery": (200, 150),
                "heavy_armor": (200, 250),
                "archery": (200, 350),
                "dual_wielding": (300, 200),
                "shield_mastery": (300, 300)
            },
            "strategy": {
                "tactical_planning": (400, 150),
                "logistics": (400, 250),
                "siege_warfare": (400, 350),
                "cavalry_tactics": (500, 200),
                "naval_warfare": (500, 300)
            },
            "charisma": {
                "persuasion": (600, 150),
                "leadership": (600, 250),
                "intimidation": (600, 350),
                "diplomacy": (700, 200),
                "espionage": (700, 300)
            }
        }
        
    def render(self, screen, skill_tree, player):
        # 渲染技能树背景
        self.render_skill_tree_background(screen)
        
        # 渲染技能树标题
        title = self.font.render("技能树", True, (255, 255, 255))
        screen.blit(title, (60, 30))
        
        # 渲染技能连接线
        self.render_skill_connections(screen)
        
        # 渲染所有技能
        self.render_skills(screen, skill_tree, player)
        
        # 渲染选中技能的详细信息
        if self.selected_skill:
            self.render_skill_details(screen, skill_tree, player)
            
    def render_skill_tree_background(self, screen):
        # 创建半透明黑色背景
        overlay = pygame.Surface((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # 渲染技能树面板
        pygame.draw.rect(screen, (50, 50, 50), self.skill_tree_rect)
        
    def render_skill_connections(self, screen):
        # 渲染技能之间的连接线
        for skill_type, skills in self.skill_positions.items():
            for skill_id, pos in skills.items():
                # 获取技能的前置技能
                skill = skill_tree.skills[skill_type][skill_id]
                if hasattr(skill, 'prerequisites'):
                    for prereq in skill.prerequisites:
                        if prereq in self.skill_positions[skill_type]:
                            start_pos = self.skill_positions[skill_type][prereq]
                            end_pos = pos
                            pygame.draw.line(screen, (100, 100, 100),
                                          start_pos, end_pos, 2)
                            
    def render_skills(self, screen, skill_tree, player):
        # 渲染所有技能
        for skill_type, skills in self.skill_positions.items():
            for skill_id, pos in skills.items():
                skill = skill_tree.skills[skill_type][skill_id]
                
                # 确定技能状态颜色
                if skill.is_unlocked:
                    color = (0, 255, 0)  # 已解锁
                elif skill.can_unlock(player):
                    color = (255, 255, 0)  # 可解锁
                else:
                    color = (100, 100, 100)  # 未解锁
                    
                # 绘制技能圆圈
                pygame.draw.circle(screen, color, pos, self.skill_radius)
                
                # 绘制技能名称
                skill_text = self.small_font.render(skill.name[:2], True, (255, 255, 255))
                text_rect = skill_text.get_rect(center=pos)
                screen.blit(skill_text, text_rect)
                
                # 如果技能被选中，绘制高亮边框
                if skill_id == self.selected_skill:
                    pygame.draw.circle(screen, (255, 255, 0),
                                    pos, self.skill_radius + 3, 2)
                    
    def render_skill_details(self, screen, skill_tree, player):
        if self.selected_skill:
            # 查找选中的技能
            for skill_type, skills in skill_tree.skills.items():
                if self.selected_skill in skills:
                    skill = skills[self.selected_skill]
                    
                    # 创建详细信息面板
                    details_rect = pygame.Rect(400, 70, 300, 200)
                    pygame.draw.rect(screen, (50, 50, 50), details_rect)
                    
                    # 渲染技能名称
                    name_text = self.font.render(skill.name, True, (255, 255, 255))
                    screen.blit(name_text, (420, 90))
                    
                    # 渲染技能描述
                    desc_text = self.small_font.render(skill.description, True, (200, 200, 200))
                    screen.blit(desc_text, (420, 130))
                    
                    # 渲染技能要求
                    req_text = self.small_font.render(
                        f"等级要求: {skill.level_requirement}",
                        True, (200, 200, 200)
                    )
                    screen.blit(req_text, (420, 160))
                    
                    # 渲染技能效果
                    for effect, value in skill.effects.items():
                        effect_text = self.small_font.render(
                            f"{effect}: {value}",
                            True, (200, 200, 200)
                        )
                        screen.blit(effect_text, (420, 190))
                        
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击了技能
            for skill_type, skills in self.skill_positions.items():
                for skill_id, pos in skills.items():
                    # 计算点击位置与技能中心的距离
                    distance = ((event.pos[0] - pos[0]) ** 2 + 
                              (event.pos[1] - pos[1]) ** 2) ** 0.5
                    if distance <= self.skill_radius:
                        self.selected_skill = skill_id
                        return "select_skill", skill_id
                        
        return None, None 