import pygame
from typing import Dict, List, Optional
from ..core.resource_manager import ResourceManager
from ..core.item_system import Item, Weapon, Armor
from ..core.skill_system import Skill, SkillTree

class Player:
    def __init__(self, config, resource_manager: ResourceManager):
        self.config = config
        self.resource_manager = resource_manager
        
        # 基本属性
        self.name = "琼恩·雪诺"
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        
        # 战斗属性
        self.max_health = 100
        self.current_health = 100
        self.max_mana = 50
        self.current_mana = 50
        self.strength = 10
        self.dexterity = 8
        self.intelligence = 6
        self.vitality = 8
        
        # 装备
        self.equipped_weapon: Optional[Weapon] = None
        self.equipped_armor: Optional[Armor] = None
        
        # 物品栏
        self.inventory: List[Item] = []
        self.inventory_size = 25
        
        # 技能
        self.skill_tree = SkillTree()
        self.available_skill_points = 0
        
        # 位置和移动
        self.x = 0
        self.y = 0
        self.direction = "down"  # up, down, left, right
        self.is_moving = False
        self.movement_speed = config.PLAYER_SPEED
        
        # 动画
        self.current_animation = None
        self.animation_frame = 0
        self.animation_timer = 0
        self.load_animations()
        
    def load_animations(self):
        """加载角色动画"""
        self.animations = {
            "idle": self.resource_manager.get_animation("player_idle"),
            "walk": self.resource_manager.get_animation("player_walk"),
            "attack": self.resource_manager.get_animation("player_attack"),
            "cast": self.resource_manager.get_animation("player_cast")
        }
        
    def update(self, delta_time: float):
        """更新玩家状态"""
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
            
    def move(self, direction: str):
        """移动角色"""
        self.direction = direction
        self.is_moving = True
        self.current_animation = self.animations["walk"]
        
    def stop_moving(self):
        """停止移动"""
        self.is_moving = False
        self.current_animation = self.animations["idle"]
        
    def attack(self):
        """攻击动作"""
        if self.equipped_weapon:
            self.current_animation = self.animations["attack"]
            return {
                "damage": self.calculate_damage(),
                "range": self.equipped_weapon.range,
                "effects": self.equipped_weapon.effects
            }
        return None
        
    def cast_skill(self, skill: Skill):
        """施放技能"""
        if self.current_mana >= skill.mana_cost:
            self.current_mana -= skill.mana_cost
            self.current_animation = self.animations["cast"]
            return skill.effects
        return None
        
    def calculate_damage(self) -> int:
        """计算伤害"""
        base_damage = self.equipped_weapon.damage if self.equipped_weapon else 5
        strength_bonus = self.strength * 0.5
        return int(base_damage + strength_bonus)
        
    def take_damage(self, damage: int) -> bool:
        """受到伤害"""
        defense = self.equipped_armor.defense if self.equipped_armor else 0
        actual_damage = max(1, damage - defense)
        self.current_health = max(0, self.current_health - actual_damage)
        return self.current_health <= 0
        
    def heal(self, amount: int):
        """恢复生命值"""
        self.current_health = min(self.max_health, self.current_health + amount)
        
    def restore_mana(self, amount: int):
        """恢复法力值"""
        self.current_mana = min(self.max_mana, self.current_mana + amount)
        
    def gain_experience(self, amount: int):
        """获得经验值"""
        self.experience += amount
        while self.experience >= self.experience_to_next_level:
            self.level_up()
            
    def level_up(self):
        """升级"""
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
        self.available_skill_points += 1
        
        # 提升属性
        self.max_health += 10
        self.current_health = self.max_health
        self.max_mana += 5
        self.current_mana = self.max_mana
        
    def equip_item(self, item: Item) -> bool:
        """装备物品"""
        if isinstance(item, Weapon):
            if self.equipped_weapon:
                self.unequip_item(self.equipped_weapon)
            self.equipped_weapon = item
            return True
        elif isinstance(item, Armor):
            if self.equipped_armor:
                self.unequip_item(self.equipped_armor)
            self.equipped_armor = item
            return True
        return False
        
    def unequip_item(self, item: Item):
        """卸下装备"""
        if item == self.equipped_weapon:
            self.equipped_weapon = None
        elif item == self.equipped_armor:
            self.equipped_armor = None
            
    def add_to_inventory(self, item: Item) -> bool:
        """添加物品到物品栏"""
        if len(self.inventory) < self.inventory_size:
            self.inventory.append(item)
            return True
        return False
        
    def remove_from_inventory(self, item: Item):
        """从物品栏移除物品"""
        if item in self.inventory:
            self.inventory.remove(item)
            
    def render(self, screen: pygame.Surface, camera):
        """渲染玩家"""
        if self.current_animation:
            frame = self.current_animation.frames[self.animation_frame]
            screen_pos = camera.apply((self.x, self.y))
            screen.blit(frame, screen_pos) 