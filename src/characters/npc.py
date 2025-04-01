import pygame
from typing import Dict, List, Optional
from ..core.resource_manager import ResourceManager
from ..core.dialogue_system import DialogueNode

class NPC:
    def __init__(self, config, resource_manager: ResourceManager, npc_data: Dict):
        self.config = config
        self.resource_manager = resource_manager
        
        # 基本属性
        self.id = npc_data["id"]
        self.name = npc_data["name"]
        self.npc_type = npc_data["type"]  # merchant, quest_giver, companion等
        
        # 位置和移动
        self.x = npc_data["x"]
        self.y = npc_data["y"]
        self.direction = "down"
        self.is_moving = False
        self.movement_speed = config.PLAYER_SPEED * 0.5
        
        # 对话系统
        self.dialogue_tree = self.load_dialogue_tree(npc_data.get("dialogue_tree", {}))
        self.current_dialogue = None
        
        # 任务相关
        self.available_quests = npc_data.get("quests", [])
        self.completed_quests = []
        
        # 商店（如果是商人）
        self.shop_inventory = npc_data.get("shop_inventory", [])
        
        # 动画
        self.current_animation = None
        self.animation_frame = 0
        self.animation_timer = 0
        self.load_animations()
        
    def load_animations(self):
        """加载NPC动画"""
        self.animations = {
            "idle": self.resource_manager.get_animation(f"{self.npc_type}_idle"),
            "walk": self.resource_manager.get_animation(f"{self.npc_type}_walk"),
            "talk": self.resource_manager.get_animation(f"{self.npc_type}_talk")
        }
        
    def load_dialogue_tree(self, dialogue_data: Dict) -> Dict[str, DialogueNode]:
        """加载对话树"""
        dialogue_tree = {}
        for node_id, node_data in dialogue_data.items():
            dialogue_tree[node_id] = DialogueNode(
                id=node_id,
                text=node_data["text"],
                options=node_data.get("options", []),
                effects=node_data.get("effects", {})
            )
        return dialogue_tree
        
    def update(self, delta_time: float):
        """更新NPC状态"""
        # 更新动画
        if self.current_animation:
            self.animation_timer += delta_time
            if self.animation_timer >= self.current_animation.frame_duration:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % len(self.current_animation.frames)
                
        # 更新移动
        if self.is_moving:
            self.update_position(delta_time)
            
    def update_position(self, delta_time: float):
        """更新位置"""
        speed = self.movement_speed * delta_time
        if self.direction == "up":
            self.y -= speed
        elif self.direction == "down":
            self.y += speed
        elif self.direction == "left":
            self.x -= speed
        elif self.direction == "right":
            self.x += speed
            
    def start_dialogue(self, player) -> Optional[DialogueNode]:
        """开始对话"""
        self.current_animation = self.animations["talk"]
        return self.dialogue_tree.get("start")
        
    def end_dialogue(self):
        """结束对话"""
        self.current_animation = self.animations["idle"]
        self.current_dialogue = None
        
    def get_dialogue_option(self, option_id: str) -> Optional[DialogueNode]:
        """获取对话选项"""
        if self.current_dialogue and option_id in self.current_dialogue.options:
            return self.dialogue_tree.get(option_id)
        return None
        
    def has_available_quests(self) -> bool:
        """检查是否有可用任务"""
        return len(self.available_quests) > 0
        
    def get_available_quests(self) -> List[Dict]:
        """获取可用任务列表"""
        return self.available_quests
        
    def complete_quest(self, quest_id: str):
        """完成任务"""
        for quest in self.available_quests:
            if quest["id"] == quest_id:
                self.completed_quests.append(quest)
                self.available_quests.remove(quest)
                break
                
    def is_merchant(self) -> bool:
        """检查是否是商人"""
        return self.npc_type == "merchant"
        
    def get_shop_inventory(self) -> List[Dict]:
        """获取商店物品列表"""
        return self.shop_inventory if self.is_merchant() else []
        
    def render(self, screen: pygame.Surface, camera):
        """渲染NPC"""
        if self.current_animation:
            frame = self.current_animation.frames[self.animation_frame]
            screen_pos = camera.apply((self.x, self.y))
            screen.blit(frame, screen_pos) 