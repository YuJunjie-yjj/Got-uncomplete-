from enum import Enum
from typing import Dict, Any

class GameState(Enum):
    MAIN_MENU = "main_menu"
    PLAYING = "playing"
    PAUSED = "paused"
    COMBAT = "combat"
    DIALOGUE = "dialogue"
    INVENTORY = "inventory"
    SKILL_TREE = "skill_tree"
    QUEST_LOG = "quest_log"
    GAME_OVER = "game_over"

class GameStateManager:
    def __init__(self):
        self.current_state = GameState.MAIN_MENU
        self.previous_state = None
        self.state_data: Dict[str, Any] = {}
        
    def change_state(self, new_state: GameState, **kwargs):
        """改变游戏状态"""
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_data = kwargs
        
    def revert_state(self):
        """恢复到上一个状态"""
        if self.previous_state:
            self.current_state, self.previous_state = self.previous_state, self.current_state
            
    def get_state_data(self) -> Dict[str, Any]:
        """获取当前状态的数据"""
        return self.state_data
        
    def is_state(self, state: GameState) -> bool:
        """检查当前是否处于指定状态"""
        return self.current_state == state
        
    def is_combat(self) -> bool:
        """检查是否在战斗中"""
        return self.is_state(GameState.COMBAT)
        
    def is_dialogue(self) -> bool:
        """检查是否在对话中"""
        return self.is_state(GameState.DIALOGUE)
        
    def is_inventory(self) -> bool:
        """检查是否在物品栏中"""
        return self.is_state(GameState.INVENTORY)
        
    def is_skill_tree(self) -> bool:
        """检查是否在技能树中"""
        return self.is_state(GameState.SKILL_TREE)
        
    def is_quest_log(self) -> bool:
        """检查是否在任务日志中"""
        return self.is_state(GameState.QUEST_LOG)
        
    def is_paused(self) -> bool:
        """检查游戏是否暂停"""
        return self.is_state(GameState.PAUSED)
        
    def is_game_over(self) -> bool:
        """检查游戏是否结束"""
        return self.is_state(GameState.GAME_OVER) 