import pygame
import sys
from typing import Optional

from .game_state import GameState, GameStateManager
from .event_system import EventSystem
from .resource_manager import ResourceManager
from .audio_system import AudioSystem
from .map_system import MapSystem
from .camera import Camera
from .weather_system import WeatherSystem
from .time_system import TimeSystem
from .combat_ui import CombatUI
from .inventory_ui import InventoryUI
from .skill_tree_ui import SkillTreeUI
from .quest_ui import QuestUI

class Game:
    def __init__(self, config):
        self.config = config
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("权力的游戏")
        
        # 初始化各个系统
        self.state_manager = GameStateManager()
        self.event_system = EventSystem()
        self.resource_manager = ResourceManager(config)
        self.audio_system = AudioSystem(config)
        self.map_system = MapSystem(config)
        self.camera = Camera(config)
        self.weather_system = WeatherSystem(config)
        self.time_system = TimeSystem(config)
        
        # 初始化UI系统
        self.combat_ui = CombatUI(config)
        self.inventory_ui = InventoryUI(config)
        self.skill_tree_ui = SkillTreeUI(config)
        self.quest_ui = QuestUI(config)
        
        # 游戏时钟
        self.clock = pygame.time.Clock()
        self.running = True
        
        # 初始化事件系统
        self.event_system.create_game_events()
        
    def run(self):
        """游戏主循环"""
        while self.running:
            # 处理事件
            self.handle_events()
            
            # 更新游戏状态
            self.update()
            
            # 渲染画面
            self.render()
            
            # 控制帧率
            self.clock.tick(self.config.FPS)
            
    def handle_events(self):
        """处理游戏事件"""
        # 处理Pygame事件
        self.event_system.handle_pygame_events()
        
        # 处理游戏事件
        self.event_system.handle_events()
        
    def update(self):
        """更新游戏状态"""
        # 更新天气系统
        self.weather_system.update(self.clock.get_time() / 1000.0)
        
        # 更新时间系统
        self.time_system.update(self.clock.get_time() / 1000.0)
        
        # 根据当前状态更新相应的系统
        if self.state_manager.is_state(GameState.PLAYING):
            self.update_gameplay()
        elif self.state_manager.is_state(GameState.COMBAT):
            self.update_combat()
        elif self.state_manager.is_state(GameState.DIALOGUE):
            self.update_dialogue()
            
    def update_gameplay(self):
        """更新游戏玩法状态"""
        # 更新相机
        self.camera.update()
        
        # 更新玩家
        # TODO: 实现玩家更新逻辑
        
        # 更新NPC
        # TODO: 实现NPC更新逻辑
        
    def update_combat(self):
        """更新战斗状态"""
        # TODO: 实现战斗更新逻辑
        pass
        
    def update_dialogue(self):
        """更新对话状态"""
        # TODO: 实现对话更新逻辑
        pass
        
    def render(self):
        """渲染游戏画面"""
        # 清空屏幕
        self.screen.fill((0, 0, 0))
        
        # 根据当前状态渲染相应的画面
        if self.state_manager.is_state(GameState.MAIN_MENU):
            self.render_main_menu()
        elif self.state_manager.is_state(GameState.PLAYING):
            self.render_gameplay()
        elif self.state_manager.is_state(GameState.COMBAT):
            self.render_combat()
        elif self.state_manager.is_state(GameState.DIALOGUE):
            self.render_dialogue()
        elif self.state_manager.is_state(GameState.INVENTORY):
            self.render_inventory()
        elif self.state_manager.is_state(GameState.SKILL_TREE):
            self.render_skill_tree()
        elif self.state_manager.is_state(GameState.QUEST_LOG):
            self.render_quest_log()
        elif self.state_manager.is_state(GameState.GAME_OVER):
            self.render_game_over()
            
        # 更新显示
        pygame.display.flip()
        
    def render_main_menu(self):
        """渲染主菜单"""
        # TODO: 实现主菜单渲染逻辑
        pass
        
    def render_gameplay(self):
        """渲染游戏画面"""
        # 渲染地图
        self.map_system.render(self.screen, self.camera)
        
        # 渲染NPC
        self.map_system.render_npcs(self.screen, self.camera)
        
        # 渲染天气效果
        self.weather_system.render(self.screen)
        
        # 渲染时间效果
        self.time_system.render(self.screen)
        
        # 渲染玩家
        # TODO: 实现玩家渲染逻辑
        
    def render_combat(self):
        """渲染战斗画面"""
        # 渲染战斗UI
        self.combat_ui.render(self.screen, None, None)  # TODO: 传入实际的战斗系统和玩家对象
        
    def render_dialogue(self):
        """渲染对话画面"""
        # TODO: 实现对话渲染逻辑
        pass
        
    def render_inventory(self):
        """渲染物品栏"""
        # 渲染物品栏UI
        self.inventory_ui.render(self.screen, None)  # TODO: 传入实际的玩家对象
        
    def render_skill_tree(self):
        """渲染技能树"""
        # 渲染技能树UI
        self.skill_tree_ui.render(self.screen, None, None)  # TODO: 传入实际的技能树和玩家对象
        
    def render_quest_log(self):
        """渲染任务日志"""
        # 渲染任务日志UI
        self.quest_ui.render(self.screen, None)  # TODO: 传入实际的故事管理器
        
    def render_game_over(self):
        """渲染游戏结束画面"""
        # TODO: 实现游戏结束画面渲染逻辑
        pass
        
    def quit(self):
        """退出游戏"""
        self.running = False
        pygame.quit()
        sys.exit() 