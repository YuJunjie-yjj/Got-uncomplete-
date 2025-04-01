class Skill:
    def __init__(self, id, name, description, skill_type, level_requirement, 
                 experience_cost, effects=None):
        self.id = id
        self.name = name
        self.description = description
        self.skill_type = skill_type  # combat, strategy, charisma
        self.level_requirement = level_requirement
        self.experience_cost = experience_cost
        self.effects = effects or {}
        self.is_unlocked = False
        
    def can_unlock(self, player):
        return (player.level >= self.level_requirement and 
                player.experience >= self.experience_cost)
        
    def unlock(self, player):
        if self.can_unlock(player):
            player.experience -= self.experience_cost
            self.is_unlocked = True
            return True
        return False
        
    def apply_effects(self, player):
        for effect, value in self.effects.items():
            if effect == "damage_bonus":
                player.damage_bonus += value
            elif effect == "defense_bonus":
                player.defense_bonus += value
            elif effect == "speed_bonus":
                player.speed_bonus += value
            elif effect == "health_bonus":
                player.max_health += value
                player.health += value

class SkillTree:
    def __init__(self):
        self.skills = {}
        self.load_skills()
        
    def load_skills(self):
        # TODO: 从JSON文件加载技能数据
        self.skills = {
            "combat": {
                "sword_mastery": Skill(
                    "sword_mastery",
                    "剑术精通",
                    "提高剑术伤害和攻击速度",
                    "combat",
                    1,
                    100,
                    {"damage_bonus": 10, "attack_speed": 1.1}
                ),
                "heavy_armor": Skill(
                    "heavy_armor",
                    "重甲专精",
                    "提高重甲防御效果",
                    "combat",
                    5,
                    200,
                    {"defense_bonus": 15}
                )
            },
            "strategy": {
                "tactical_planning": Skill(
                    "tactical_planning",
                    "战术规划",
                    "提高部队指挥能力",
                    "strategy",
                    3,
                    150,
                    {"command_bonus": 20}
                ),
                "logistics": Skill(
                    "logistics",
                    "后勤管理",
                    "提高资源管理效率",
                    "strategy",
                    7,
                    300,
                    {"resource_efficiency": 25}
                )
            },
            "charisma": {
                "persuasion": Skill(
                    "persuasion",
                    "说服力",
                    "提高对话选项成功率",
                    "charisma",
                    2,
                    120,
                    {"dialogue_success": 15}
                ),
                "leadership": Skill(
                    "leadership",
                    "领导力",
                    "提高部队士气",
                    "charisma",
                    6,
                    250,
                    {"morale_bonus": 20}
                )
            }
        }
        
    def get_available_skills(self, player):
        available = {}
        for skill_type, skills in self.skills.items():
            available[skill_type] = [
                skill for skill in skills.values()
                if not skill.is_unlocked and skill.can_unlock(player)
            ]
        return available
        
    def get_unlocked_skills(self, player):
        unlocked = {}
        for skill_type, skills in self.skills.items():
            unlocked[skill_type] = [
                skill for skill in skills.values()
                if skill.is_unlocked
            ]
        return unlocked
        
    def unlock_skill(self, player, skill_id):
        for skill_type, skills in self.skills.items():
            if skill_id in skills:
                skill = skills[skill_id]
                if skill.unlock(player):
                    skill.apply_effects(player)
                    return True
        return False 