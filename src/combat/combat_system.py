import pygame
from typing import List, Dict, Optional
from ..characters.player import Player
from ..characters.npc import NPC
from ..core.event_system import EventSystem

class CombatSystem:
    def __init__(self, config, event_system: EventSystem):
        self.config = config
        self.event_system = event_system
        
        # 战斗状态
        self.is_active = False
        self.turn_order: List[Player | NPC] = []
        self.current_turn = 0
        self.turn_timer = 0
        
        # 战斗者
        self.player: Optional[Player] = None
        self.enemies: List[NPC] = []
        
        # 战斗UI状态
        self.selected_action = None
        self.selected_target = None
        self.action_menu_open = False
        self.target_menu_open = False
        
    def start_combat(self, player: Player, enemies: List[NPC]):
        """开始战斗"""
        self.is_active = True
        self.player = player
        self.enemies = enemies
        
        # 初始化回合顺序
        self.turn_order = [player] + enemies
        self.current_turn = 0
        self.turn_timer = 0
        
        # 触发战斗开始事件
        self.event_system.trigger_event("combat_start", 
                                      enemy_names=[enemy.name for enemy in enemies])
        
    def end_combat(self, victory: bool):
        """结束战斗"""
        self.is_active = False
        self.player = None
        self.enemies = []
        self.turn_order = []
        
        # 触发战斗结束事件
        self.event_system.trigger_event("combat_end", victory=victory)
        
    def update(self, delta_time: float):
        """更新战斗状态"""
        if not self.is_active:
            return
            
        # 更新回合计时器
        self.turn_timer += delta_time
        
        # 检查回合是否结束
        if self.turn_timer >= self.config.COMBAT_TURN_TIME:
            self.next_turn()
            
    def next_turn(self):
        """进入下一个回合"""
        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        self.turn_timer = 0
        
        # 触发回合事件
        current_actor = self.turn_order[self.current_turn]
        self.event_system.trigger_event("combat_turn",
                                      turn_number=self.current_turn + 1,
                                      actor_name=current_actor.name)
        
        # 如果是敌人回合，执行AI行动
        if isinstance(current_actor, NPC):
            self.execute_enemy_turn(current_actor)
            
    def execute_enemy_turn(self, enemy: NPC):
        """执行敌人回合"""
        # 简单的AI：随机选择目标并攻击
        target = self.player
        damage = self.calculate_damage(enemy, target)
        self.apply_damage(enemy, target, damage)
        
    def select_action(self, action: str):
        """选择行动"""
        self.selected_action = action
        self.action_menu_open = False
        self.target_menu_open = True
        
    def select_target(self, target: Player | NPC):
        """选择目标"""
        if not self.selected_action:
            return
            
        self.selected_target = target
        self.target_menu_open = False
        
        # 执行行动
        if self.selected_action == "attack":
            damage = self.calculate_damage(self.player, target)
            self.apply_damage(self.player, target, damage)
        elif self.selected_action == "skill":
            # TODO: 实现技能系统
            pass
            
        # 重置选择
        self.selected_action = None
        self.selected_target = None
        
    def calculate_damage(self, attacker: Player | NPC, target: Player | NPC) -> int:
        """计算伤害"""
        if isinstance(attacker, Player):
            return attacker.calculate_damage()
        else:
            # NPC基础伤害
            return 10
            
    def apply_damage(self, attacker: Player | NPC, target: Player | NPC, damage: int):
        """应用伤害"""
        is_dead = target.take_damage(damage)
        
        # 触发伤害事件
        self.event_system.trigger_event("damage_dealt",
                                      attacker=attacker.name,
                                      target=target.name,
                                      damage=damage)
        
        # 检查目标是否死亡
        if is_dead:
            self.handle_combatant_death(target)
            
    def handle_combatant_death(self, combatant: Player | NPC):
        """处理战斗者死亡"""
        # 从回合顺序中移除
        if combatant in self.turn_order:
            self.turn_order.remove(combatant)
            
        # 如果是敌人，从敌人列表中移除
        if combatant in self.enemies:
            self.enemies.remove(combatant)
            
        # 检查战斗是否结束
        if not self.enemies:
            self.end_combat(True)
        elif isinstance(combatant, Player):
            self.end_combat(False)
            
    def get_current_actor(self) -> Player | NPC:
        """获取当前回合的行动者"""
        if not self.turn_order:
            return None
        return self.turn_order[self.current_turn]
        
    def is_player_turn(self) -> bool:
        """检查是否是玩家回合"""
        return isinstance(self.get_current_actor(), Player)
        
    def get_available_actions(self) -> List[str]:
        """获取可用行动列表"""
        if not self.is_player_turn():
            return []
            
        actions = ["attack"]
        # TODO: 添加技能检查
        return actions
        
    def get_valid_targets(self, action: str) -> List[Player | NPC]:
        """获取有效目标列表"""
        if action == "attack":
            return self.enemies
        # TODO: 添加其他行动的目标检查
        return [] 