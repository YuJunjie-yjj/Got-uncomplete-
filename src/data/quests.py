QUEST_DATA = {
    "tutorial_quest": {
        "id": "tutorial_quest",
        "title": "新手训练",
        "description": "在临冬城完成基本训练，成为一名合格的守夜人。",
        "objectives": [
            {
                "id": "talk_to_maester",
                "description": "与学士交谈",
                "required": 1
            },
            {
                "id": "practice_combat",
                "description": "完成基础战斗训练",
                "required": 3
            },
            {
                "id": "learn_skills",
                "description": "学习基本技能",
                "required": 2
            }
        ],
        "rewards": {
            "experience": 100,
            "items": ["basic_sword", "leather_armor"],
            "gold": 50
        },
        "prerequisites": [],
        "next_quests": ["first_ranging"]
    },
    
    "first_ranging": {
        "id": "first_ranging",
        "title": "首次巡逻",
        "description": "加入守夜人巡逻队，探索长城以北的区域。",
        "objectives": [
            {
                "id": "join_patrol",
                "description": "加入巡逻队",
                "required": 1
            },
            {
                "id": "explore_area",
                "description": "探索指定区域",
                "required": 5
            },
            {
                "id": "defeat_wildlings",
                "description": "击败野人",
                "required": 3
            }
        ],
        "rewards": {
            "experience": 200,
            "items": ["dragonglass_dagger"],
            "gold": 100
        },
        "prerequisites": ["tutorial_quest"],
        "next_quests": ["investigate_white_walkers"]
    },
    
    "investigate_white_walkers": {
        "id": "investigate_white_walkers",
        "title": "异鬼调查",
        "description": "调查异鬼的踪迹，寻找他们的弱点。",
        "objectives": [
            {
                "id": "find_evidence",
                "description": "寻找异鬼活动的证据",
                "required": 3
            },
            {
                "id": "defeat_wights",
                "description": "击败尸鬼",
                "required": 5
            },
            {
                "id": "report_findings",
                "description": "向指挥官报告发现",
                "required": 1
            }
        ],
        "rewards": {
            "experience": 300,
            "items": ["valyrian_steel_sword"],
            "gold": 200
        },
        "prerequisites": ["first_ranging"],
        "next_quests": ["prepare_for_battle"]
    },
    
    "prepare_for_battle": {
        "id": "prepare_for_battle",
        "title": "备战",
        "description": "为即将到来的大战做准备，收集资源并训练军队。",
        "objectives": [
            {
                "id": "gather_resources",
                "description": "收集战争物资",
                "required": 10
            },
            {
                "id": "train_army",
                "description": "训练军队",
                "required": 5
            },
            {
                "id": "fortify_defenses",
                "description": "加固防御工事",
                "required": 3
            }
        ],
        "rewards": {
            "experience": 400,
            "items": ["dragon_glass_armor"],
            "gold": 300
        },
        "prerequisites": ["investigate_white_walkers"],
        "next_quests": ["final_battle"]
    },
    
    "final_battle": {
        "id": "final_battle",
        "title": "最终之战",
        "description": "与异鬼大军展开决战，保卫维斯特洛。",
        "objectives": [
            {
                "id": "defeat_white_walkers",
                "description": "击败异鬼将领",
                "required": 3
            },
            {
                "id": "protect_castle",
                "description": "保护城堡不被攻陷",
                "required": 1
            },
            {
                "id": "defeat_night_king",
                "description": "击败夜王",
                "required": 1
            }
        ],
        "rewards": {
            "experience": 1000,
            "items": ["legendary_sword", "legendary_armor"],
            "gold": 1000
        },
        "prerequisites": ["prepare_for_battle"],
        "next_quests": []
    }
} 