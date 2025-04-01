import pygame
import json

class DialogueOption:
    def __init__(self, text, next_node, requirements=None, consequences=None):
        self.text = text
        self.next_node = next_node
        self.requirements = requirements or {}
        self.consequences = consequences or {}
        
    def is_available(self, player):
        # 检查选项是否可用
        for attr, value in self.requirements.items():
            if getattr(player, attr) < value:
                return False
        return True
        
    def apply_consequences(self, player, world, story_manager):
        # 应用选项的后果
        for attr, value in self.consequences.items():
            if attr == "reputation":
                for region, amount in value.items():
                    player.update_reputation(region, amount)
            elif attr == "experience":
                player.gain_experience(value)
            elif attr == "quest":
                story_manager.activate_quest(value)
            elif attr == "item":
                player.add_item(value)

class DialogueNode:
    def __init__(self, id, text, speaker, options=None):
        self.id = id
        self.text = text
        self.speaker = speaker
        self.options = options or []
        
    def get_available_options(self, player):
        return [opt for opt in self.options if opt.is_available(player)]

class DialogueSystem:
    def __init__(self, config):
        self.config = config
        self.current_node = None
        self.dialogue_history = []
        self.is_active = False
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # 加载对话数据
        self.load_dialogues()
        
    def load_dialogues(self):
        # TODO: 从JSON文件加载对话数据
        self.dialogues = {
            "jon_snow_intro": DialogueNode(
                "jon_snow_intro",
                "你准备好加入守夜人了吗？",
                "杰奥·莫尔蒙",
                [
                    DialogueOption(
                        "是的，我准备好了。",
                        "jon_snow_training",
                        consequences={"quest": "jon_1"}
                    ),
                    DialogueOption(
                        "让我再考虑一下。",
                        "jon_snow_intro",
                        consequences={"reputation": {"north": -10}}
                    )
                ]
            ),
            "daenerys_intro": DialogueNode(
                "daenerys_intro",
                "我是龙之母，不焚者，弥林女王。",
                "丹妮莉丝·坦格利安",
                [
                    DialogueOption(
                        "我愿为您效劳。",
                        "daenerys_quest",
                        consequences={"quest": "dany_1"}
                    ),
                    DialogueOption(
                        "我需要更多信息。",
                        "daenerys_info"
                    )
                ]
            )
        }
        
    def start_dialogue(self, dialogue_id):
        if dialogue_id in self.dialogues:
            self.current_node = self.dialogues[dialogue_id]
            self.dialogue_history = []
            self.is_active = True
            return True
        return False
        
    def handle_input(self, event):
        if not self.is_active:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击了选项
            for i, option in enumerate(self.current_node.get_available_options(self.player)):
                option_rect = pygame.Rect(50, 400 + i * 50, 700, 40)
                if option_rect.collidepoint(event.pos):
                    return option
        return None
        
    def select_option(self, option):
        # 应用选项的后果
        option.apply_consequences(self.player, self.world, self.story_manager)
        
        # 记录对话历史
        self.dialogue_history.append({
            "speaker": self.current_node.speaker,
            "text": self.current_node.text,
            "choice": option.text
        })
        
        # 移动到下一个节点
        if option.next_node in self.dialogues:
            self.current_node = self.dialogues[option.next_node]
        else:
            self.end_dialogue()
            
    def end_dialogue(self):
        self.is_active = False
        self.current_node = None
        
    def render(self, screen):
        if not self.is_active:
            return
            
        # 渲染对话背景
        pygame.draw.rect(screen, (0, 0, 0, 180), 
                        (0, 0, self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        
        # 渲染说话者名字
        speaker_text = self.font.render(self.current_node.speaker, True, (255, 255, 255))
        screen.blit(speaker_text, (50, 300))
        
        # 渲染对话文本
        text = self.font.render(self.current_node.text, True, (255, 255, 255))
        screen.blit(text, (50, 350))
        
        # 渲染选项
        for i, option in enumerate(self.current_node.get_available_options(self.player)):
            option_text = self.small_font.render(option.text, True, (200, 200, 200))
            screen.blit(option_text, (70, 410 + i * 50))
            
        # 渲染对话历史
        for i, history in enumerate(self.dialogue_history[-3:]):  # 只显示最近3条对话
            history_text = self.small_font.render(
                f"{history['speaker']}: {history['text']}", 
                True, (150, 150, 150)
            )
            screen.blit(history_text, (50, 50 + i * 30)) 