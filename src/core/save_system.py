import json
import os
from datetime import datetime

class SaveSystem:
    def __init__(self, config):
        self.config = config
        self.save_dir = "saves"
        self.ensure_save_directory()
        
    def ensure_save_directory(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
    def save_game(self, player, world, story_manager):
        # 创建存档数据
        save_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "player": {
                "name": player.name,
                "level": player.level,
                "experience": player.experience,
                "health": player.health,
                "position": [player.position.x, player.position.y],
                "attributes": {
                    "strength": player.strength,
                    "agility": player.agility,
                    "intelligence": player.intelligence,
                    "charisma": player.charisma
                },
                "equipment": {
                    "weapon": player.equipment["weapon"].to_dict() if player.equipment["weapon"] else None,
                    "armor": player.equipment["armor"].to_dict() if player.equipment["armor"] else None,
                    "accessories": [item.to_dict() for item in player.equipment["accessories"]]
                }
            },
            "world": {
                "time_of_day": world.time_of_day,
                "weather": world.weather,
                "season": world.season
            },
            "story": {
                "current_story": story_manager.current_story["id"] if story_manager.current_story else None,
                "story_progress": story_manager.story_progress,
                "active_quests": [quest["id"] for quest in story_manager.active_quests],
                "completed_quests": [quest["id"] for quest in story_manager.completed_quests]
            }
        }
        
        # 生成存档文件名
        filename = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.save_dir, filename)
        
        # 保存到文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)
            
        return filename
        
    def load_game(self, filename):
        filepath = os.path.join(self.save_dir, filename)
        if not os.path.exists(filepath):
            return None
            
        with open(filepath, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
            
        return save_data
        
    def get_save_files(self):
        saves = []
        for filename in os.listdir(self.save_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.save_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                    saves.append({
                        "filename": filename,
                        "timestamp": save_data["timestamp"],
                        "player_name": save_data["player"]["name"],
                        "level": save_data["player"]["level"]
                    })
        return sorted(saves, key=lambda x: x["timestamp"], reverse=True)
        
    def delete_save(self, filename):
        filepath = os.path.join(self.save_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath) 