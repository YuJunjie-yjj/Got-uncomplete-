class Item:
    def __init__(self, id, name, description, item_type, value, effects=None):
        self.id = id
        self.name = name
        self.description = description
        self.item_type = item_type  # weapon, armor, accessory, consumable
        self.value = value
        self.effects = effects or {}
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "item_type": self.item_type,
            "value": self.value,
            "effects": self.effects
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data["description"],
            data["item_type"],
            data["value"],
            data["effects"]
        )

class Weapon(Item):
    def __init__(self, id, name, description, damage, attack_speed, value, effects=None):
        super().__init__(id, name, description, "weapon", value, effects)
        self.damage = damage
        self.attack_speed = attack_speed
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "damage": self.damage,
            "attack_speed": self.attack_speed
        })
        return data
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data["description"],
            data["damage"],
            data["attack_speed"],
            data["value"],
            data["effects"]
        )

class Armor(Item):
    def __init__(self, id, name, description, defense, weight, value, effects=None):
        super().__init__(id, name, description, "armor", value, effects)
        self.defense = defense
        self.weight = weight
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "defense": self.defense,
            "weight": self.weight
        })
        return data
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data["description"],
            data["defense"],
            data["weight"],
            data["value"],
            data["effects"]
        )

class ItemSystem:
    def __init__(self):
        self.items = {}
        self.load_items()
        
    def load_items(self):
        # TODO: 从JSON文件加载物品数据
        self.items = {
            "longclaw": Weapon(
                "longclaw",
                "长爪",
                "瓦雷利亚钢剑，剑柄为狼头形状",
                50,
                1.2,
                1000,
                {"ice_damage": 10}
            ),
            "stark_armor": Armor(
                "stark_armor",
                "史塔克家族铠甲",
                "北境风格的厚重铠甲",
                30,
                15,
                800,
                {"cold_resistance": 20}
            ),
            "dragonglass_dagger": Weapon(
                "dragonglass_dagger",
                "龙晶匕首",
                "用龙晶制成的匕首，对异鬼特别有效",
                20,
                1.5,
                500,
                {"white_walker_damage": 50}
            )
        }
        
    def get_item(self, item_id):
        return self.items.get(item_id)
        
    def create_item(self, item_id):
        item_data = self.items.get(item_id)
        if not item_data:
            return None
            
        if item_data.item_type == "weapon":
            return Weapon.from_dict(item_data.to_dict())
        elif item_data.item_type == "armor":
            return Armor.from_dict(item_data.to_dict())
        else:
            return Item.from_dict(item_data.to_dict())
            
    def get_items_by_type(self, item_type):
        return [item for item in self.items.values() 
                if item.item_type == item_type] 