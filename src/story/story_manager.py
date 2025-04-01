import json
import random

class StoryManager:
    def __init__(self):
        self.current_story = None
        self.story_progress = 0
        self.available_stories = []
        self.completed_stories = []
        self.active_quests = []
        self.completed_quests = []
        
        # 加载故事数据
        self.load_stories()
        
    def load_stories(self):
        # TODO: 从JSON文件加载故事数据
        self.story_data = {
            "jon_snow": {
                "title": "守夜人的誓言",
                "description": "加入守夜人，保卫长城",
                "quests": [
                    {
                        "id": "jon_1",
                        "title": "新兵训练",
                        "description": "完成基础训练",
                        "objectives": ["完成剑术训练", "完成射箭训练", "完成战术训练"],
                        "rewards": {"experience": 100, "items": ["训练剑"]}
                    }
                ]
            },
            "daenerys": {
                "title": "龙之母",
                "description": "解放奴隶湾，建立新的王朝",
                "quests": [
                    {
                        "id": "dany_1",
                        "title": "解放阿斯塔波",
                        "description": "解放第一个奴隶城邦",
                        "objectives": ["潜入城市", "策反无垢者", "击败奴隶主"],
                        "rewards": {"experience": 200, "items": ["无垢者军团"]}
                    }
                ]
            }
        }
        
    def start_story(self, story_id):
        if story_id in self.story_data:
            self.current_story = self.story_data[story_id]
            self.story_progress = 0
            self.available_stories.remove(story_id)
            return True
        return False
        
    def update(self):
        if self.current_story:
            # 检查当前任务是否完成
            self.check_quest_completion()
            
            # 更新故事进度
            self.update_story_progress()
            
    def check_quest_completion(self):
        for quest in self.active_quests:
            if self.is_quest_completed(quest):
                self.complete_quest(quest)
                
    def is_quest_completed(self, quest):
        # 检查所有目标是否完成
        return all(objective["completed"] for objective in quest["objectives"])
        
    def complete_quest(self, quest):
        # 发放奖励
        self.grant_rewards(quest["rewards"])
        
        # 更新任务状态
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)
        
        # 检查是否触发新任务
        self.check_new_quests()
        
    def grant_rewards(self, rewards):
        # TODO: 实现奖励发放系统
        pass
        
    def check_new_quests(self):
        if self.current_story:
            # 检查是否有新的任务可以触发
            for quest in self.current_story["quests"]:
                if quest["id"] not in [q["id"] for q in self.active_quests + self.completed_quests]:
                    if self.can_trigger_quest(quest):
                        self.activate_quest(quest)
                        
    def can_trigger_quest(self, quest):
        # 检查任务触发条件
        return True  # TODO: 实现具体的触发条件检查
        
    def activate_quest(self, quest):
        # 激活新任务
        quest["objectives"] = [{"description": obj, "completed": False} 
                             for obj in quest["objectives"]]
        self.active_quests.append(quest)
        
    def update_story_progress(self):
        # 更新故事进度
        if not self.active_quests and self.current_story:
            self.story_progress += 1
            if self.story_progress >= len(self.current_story["quests"]):
                self.complete_story()
                
    def complete_story(self):
        # 完成当前故事
        self.completed_stories.append(self.current_story)
        self.current_story = None
        self.story_progress = 0
        
    def get_available_stories(self):
        # 获取可用的故事列表
        return [story for story_id, story in self.story_data.items() 
                if story_id not in self.completed_stories]
        
    def get_active_quests(self):
        # 获取当前激活的任务列表
        return self.active_quests
        
    def get_completed_quests(self):
        # 获取已完成的任务列表
        return self.completed_quests
        
    def render(self, screen):
        # TODO: 实现故事UI渲染
        pass 