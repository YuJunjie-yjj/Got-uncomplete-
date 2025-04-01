class Character:
    def __init__(self):
        # 基本属性
        self.name = ""
        self.level = 1
        self.experience = 0
        self.health = 100
        self.max_health = 100
        
        # 状态
        self.is_moving = False
        self.is_attacking = False
        self.is_defending = False
        self.is_dead = False
        
        # 关系网络
        self.allies = []
        self.enemies = []
        self.neutral = []
        
        # 声望系统
        self.reputation = {
            "north": 0,
            "south": 0,
            "east": 0,
            "west": 0
        }
        
    def gain_experience(self, amount):
        self.experience += amount
        # 检查是否升级
        while self.experience >= self.get_next_level_exp():
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.experience -= self.get_next_level_exp()
        self.max_health += 10
        self.health = self.max_health
        
    def get_next_level_exp(self):
        # 简单的经验值计算公式
        return self.level * 100
        
    def die(self):
        self.is_dead = True
        self.health = 0
        
    def revive(self):
        self.is_dead = False
        self.health = self.max_health // 2
        
    def update_reputation(self, region, amount):
        if region in self.reputation:
            self.reputation[region] = max(-100, min(100, 
                self.reputation[region] + amount))
            
    def get_reputation_level(self, region):
        if region not in self.reputation:
            return "Unknown"
            
        rep = self.reputation[region]
        if rep >= 80:
            return "Exalted"
        elif rep >= 60:
            return "Honored"
        elif rep >= 40:
            return "Friendly"
        elif rep >= 20:
            return "Neutral"
        elif rep >= -20:
            return "Unfriendly"
        elif rep >= -40:
            return "Hostile"
        elif rep >= -60:
            return "Hated"
        else:
            return "Exiled" 