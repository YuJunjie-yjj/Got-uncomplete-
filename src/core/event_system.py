import pygame
from typing import Dict, List, Callable, Any

class EventSystem:
    def __init__(self):
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.event_queue: List[Dict[str, Any]] = []
        
    def add_handler(self, event_type: str, handler: Callable):
        """添加事件处理器"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        
    def remove_handler(self, event_type: str, handler: Callable):
        """移除事件处理器"""
        if event_type in self.event_handlers:
            if handler in self.event_handlers[event_type]:
                self.event_handlers[event_type].remove(handler)
                
    def trigger_event(self, event_type: str, **kwargs):
        """触发事件"""
        event_data = {
            "type": event_type,
            "data": kwargs
        }
        self.event_queue.append(event_data)
        
    def handle_events(self):
        """处理所有事件"""
        while self.event_queue:
            event = self.event_queue.pop(0)
            event_type = event["type"]
            
            if event_type in self.event_handlers:
                for handler in self.event_handlers[event_type]:
                    handler(event["data"])
                    
    def handle_pygame_events(self):
        """处理Pygame事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.trigger_event("quit")
            elif event.type == pygame.KEYDOWN:
                self.trigger_event("keydown", key=event.key)
            elif event.type == pygame.KEYUP:
                self.trigger_event("keyup", key=event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.trigger_event("mousedown", button=event.button, pos=event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.trigger_event("mouseup", button=event.button, pos=event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.trigger_event("mousemotion", pos=event.pos, rel=event.rel)
                
    def create_game_events(self):
        """创建游戏特定事件"""
        # 战斗事件
        self.add_handler("combat_start", self.handle_combat_start)
        self.add_handler("combat_end", self.handle_combat_end)
        self.add_handler("combat_turn", self.handle_combat_turn)
        self.add_handler("damage_dealt", self.handle_damage_dealt)
        self.add_handler("healing_received", self.handle_healing_received)
        
        # 任务事件
        self.add_handler("quest_started", self.handle_quest_started)
        self.add_handler("quest_completed", self.handle_quest_completed)
        self.add_handler("quest_failed", self.handle_quest_failed)
        self.add_handler("quest_updated", self.handle_quest_updated)
        
        # 对话事件
        self.add_handler("dialogue_started", self.handle_dialogue_started)
        self.add_handler("dialogue_ended", self.handle_dialogue_ended)
        self.add_handler("dialogue_choice", self.handle_dialogue_choice)
        
        # 物品事件
        self.add_handler("item_picked_up", self.handle_item_picked_up)
        self.add_handler("item_dropped", self.handle_item_dropped)
        self.add_handler("item_used", self.handle_item_used)
        
        # 技能事件
        self.add_handler("skill_learned", self.handle_skill_learned)
        self.add_handler("skill_used", self.handle_skill_used)
        self.add_handler("skill_effect_applied", self.handle_skill_effect_applied)
        
        # 天气事件
        self.add_handler("weather_changed", self.handle_weather_changed)
        self.add_handler("time_of_day_changed", self.handle_time_of_day_changed)
        self.add_handler("season_changed", self.handle_season_changed)
        
    def handle_combat_start(self, data):
        """处理战斗开始事件"""
        print(f"战斗开始: {data.get('enemy_name', '未知敌人')}")
        
    def handle_combat_end(self, data):
        """处理战斗结束事件"""
        print(f"战斗结束: {'胜利' if data.get('victory') else '失败'}")
        
    def handle_combat_turn(self, data):
        """处理战斗回合事件"""
        print(f"回合 {data.get('turn_number')}: {data.get('actor_name')} 的回合")
        
    def handle_damage_dealt(self, data):
        """处理造成伤害事件"""
        print(f"{data.get('attacker')} 对 {data.get('target')} 造成了 {data.get('damage')} 点伤害")
        
    def handle_healing_received(self, data):
        """处理治疗事件"""
        print(f"{data.get('target')} 恢复了 {data.get('amount')} 点生命值")
        
    def handle_quest_started(self, data):
        """处理任务开始事件"""
        print(f"新任务: {data.get('quest_name')}")
        
    def handle_quest_completed(self, data):
        """处理任务完成事件"""
        print(f"任务完成: {data.get('quest_name')}")
        
    def handle_quest_failed(self, data):
        """处理任务失败事件"""
        print(f"任务失败: {data.get('quest_name')}")
        
    def handle_quest_updated(self, data):
        """处理任务更新事件"""
        print(f"任务更新: {data.get('quest_name')} - {data.get('update_text')}")
        
    def handle_dialogue_started(self, data):
        """处理对话开始事件"""
        print(f"开始与 {data.get('npc_name')} 对话")
        
    def handle_dialogue_ended(self, data):
        """处理对话结束事件"""
        print(f"结束与 {data.get('npc_name')} 的对话")
        
    def handle_dialogue_choice(self, data):
        """处理对话选择事件"""
        print(f"选择: {data.get('choice_text')}")
        
    def handle_item_picked_up(self, data):
        """处理拾取物品事件"""
        print(f"拾取了 {data.get('item_name')}")
        
    def handle_item_dropped(self, data):
        """处理丢弃物品事件"""
        print(f"丢弃了 {data.get('item_name')}")
        
    def handle_item_used(self, data):
        """处理使用物品事件"""
        print(f"使用了 {data.get('item_name')}")
        
    def handle_skill_learned(self, data):
        """处理学习技能事件"""
        print(f"学会了新技能: {data.get('skill_name')}")
        
    def handle_skill_used(self, data):
        """处理使用技能事件"""
        print(f"使用了技能: {data.get('skill_name')}")
        
    def handle_skill_effect_applied(self, data):
        """处理技能效果事件"""
        print(f"技能效果: {data.get('effect_name')} 被应用到 {data.get('target')}")
        
    def handle_weather_changed(self, data):
        """处理天气变化事件"""
        print(f"天气变为: {data.get('weather_type')}")
        
    def handle_time_of_day_changed(self, data):
        """处理时间变化事件"""
        print(f"时间变为: {data.get('time_of_day')}")
        
    def handle_season_changed(self, data):
        """处理季节变化事件"""
        print(f"季节变为: {data.get('season')}") 