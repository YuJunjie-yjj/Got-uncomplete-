from typing import Dict, List, Optional
from ..core.event_system import EventSystem

class Quest:
    def __init__(self, quest_data: Dict):
        self.id = quest_data["id"]
        self.title = quest_data["title"]
        self.description = quest_data["description"]
        self.objectives = quest_data["objectives"]
        self.rewards = quest_data["rewards"]
        self.prerequisites = quest_data.get("prerequisites", [])
        self.next_quests = quest_data.get("next_quests", [])
        
        # 任务状态
        self.is_active = False
        self.is_completed = False
        self.is_failed = False
        self.progress = {objective["id"]: 0 for objective in self.objectives}
        
    def start(self):
        """开始任务"""
        self.is_active = True
        self.is_completed = False
        self.is_failed = False
        self.progress = {objective["id"]: 0 for objective in self.objectives}
        
    def update_progress(self, objective_id: str, amount: int = 1):
        """更新任务进度"""
        if not self.is_active:
            return
            
        if objective_id in self.progress:
            objective = next(obj for obj in self.objectives if obj["id"] == objective_id)
            self.progress[objective_id] = min(amount, objective["required"])
            
            # 检查是否完成所有目标
            if all(self.progress[obj["id"]] >= obj["required"] for obj in self.objectives):
                self.complete()
                
    def complete(self):
        """完成任务"""
        self.is_active = False
        self.is_completed = True
        self.is_failed = False
        
    def fail(self):
        """任务失败"""
        self.is_active = False
        self.is_completed = False
        self.is_failed = True
        
    def get_progress_text(self) -> str:
        """获取进度文本"""
        progress_texts = []
        for objective in self.objectives:
            current = self.progress[objective["id"]]
            required = objective["required"]
            progress_texts.append(f"{objective['description']}: {current}/{required}")
        return "\n".join(progress_texts)
        
class QuestSystem:
    def __init__(self, event_system: EventSystem):
        self.event_system = event_system
        self.quests: Dict[str, Quest] = {}
        self.active_quests: List[Quest] = []
        self.completed_quests: List[Quest] = []
        self.failed_quests: List[Quest] = []
        
    def load_quests(self, quest_data: Dict[str, Dict]):
        """加载任务数据"""
        for quest_id, quest_info in quest_data.items():
            self.quests[quest_id] = Quest(quest_info)
            
    def start_quest(self, quest_id: str) -> bool:
        """开始任务"""
        if quest_id not in self.quests:
            return False
            
        quest = self.quests[quest_id]
        
        # 检查前置条件
        if not self.check_prerequisites(quest):
            return False
            
        # 开始任务
        quest.start()
        self.active_quests.append(quest)
        
        # 触发任务开始事件
        self.event_system.trigger_event("quest_started",
                                      quest_name=quest.title)
        return True
        
    def complete_quest(self, quest_id: str):
        """完成任务"""
        if quest_id not in self.quests:
            return
            
        quest = self.quests[quest_id]
        if not quest.is_active:
            return
            
        quest.complete()
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)
        
        # 触发任务完成事件
        self.event_system.trigger_event("quest_completed",
                                      quest_name=quest.title)
        
        # 检查并开始后续任务
        for next_quest_id in quest.next_quests:
            self.start_quest(next_quest_id)
            
    def fail_quest(self, quest_id: str):
        """任务失败"""
        if quest_id not in self.quests:
            return
            
        quest = self.quests[quest_id]
        if not quest.is_active:
            return
            
        quest.fail()
        self.active_quests.remove(quest)
        self.failed_quests.append(quest)
        
        # 触发任务失败事件
        self.event_system.trigger_event("quest_failed",
                                      quest_name=quest.title)
        
    def update_quest_progress(self, quest_id: str, objective_id: str, amount: int = 1):
        """更新任务进度"""
        if quest_id not in self.quests:
            return
            
        quest = self.quests[quest_id]
        if not quest.is_active:
            return
            
        quest.update_progress(objective_id, amount)
        
        # 触发任务更新事件
        self.event_system.trigger_event("quest_updated",
                                      quest_name=quest.title,
                                      update_text=quest.get_progress_text())
        
    def check_prerequisites(self, quest: Quest) -> bool:
        """检查任务前置条件"""
        for prereq_id in quest.prerequisites:
            if prereq_id not in self.completed_quests:
                return False
        return True
        
    def get_available_quests(self) -> List[Quest]:
        """获取可用任务列表"""
        available = []
        for quest in self.quests.values():
            if not quest.is_active and not quest.is_completed and not quest.is_failed:
                if self.check_prerequisites(quest):
                    available.append(quest)
        return available
        
    def get_active_quests(self) -> List[Quest]:
        """获取进行中的任务列表"""
        return self.active_quests
        
    def get_completed_quests(self) -> List[Quest]:
        """获取已完成的任务列表"""
        return self.completed_quests
        
    def get_failed_quests(self) -> List[Quest]:
        """获取失败的任务列表"""
        return self.failed_quests 