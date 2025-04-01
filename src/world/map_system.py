import pygame
import pytmx
import pyscroll
import os

class MapSystem:
    def __init__(self, config):
        self.config = config
        self.current_map = None
        self.map_data = {}
        self.load_maps()
        
    def load_maps(self):
        # 加载所有地图
        maps_dir = "assets/maps"
        for filename in os.listdir(maps_dir):
            if filename.endswith('.tmx'):
                map_path = os.path.join(maps_dir, filename)
                map_name = os.path.splitext(filename)[0]
                
                # 加载TMX地图
                tmx_data = pytmx.load_pygame(map_path)
                
                # 创建地图数据
                map_data = {
                    "tmx": tmx_data,
                    "layers": [],
                    "collision_layer": None,
                    "spawn_points": [],
                    "npcs": [],
                    "triggers": []
                }
                
                # 处理地图层
                for layer in tmx_data.layers:
                    if layer.name == "collision":
                        map_data["collision_layer"] = layer
                    elif layer.name == "spawn":
                        map_data["spawn_points"] = self.extract_spawn_points(layer)
                    elif layer.name == "npc":
                        map_data["npcs"] = self.extract_npcs(layer)
                    elif layer.name == "trigger":
                        map_data["triggers"] = self.extract_triggers(layer)
                    else:
                        map_data["layers"].append(layer)
                        
                self.map_data[map_name] = map_data
                
    def extract_spawn_points(self, layer):
        spawn_points = []
        for x, y, tile in layer.tiles():
            if tile:
                spawn_points.append({
                    "x": x * self.config.TILE_SIZE,
                    "y": y * self.config.TILE_SIZE,
                    "type": tile.properties.get("type", "default")
                })
        return spawn_points
        
    def extract_npcs(self, layer):
        npcs = []
        for x, y, tile in layer.tiles():
            if tile:
                npcs.append({
                    "x": x * self.config.TILE_SIZE,
                    "y": y * self.config.TILE_SIZE,
                    "id": tile.properties.get("npc_id"),
                    "name": tile.properties.get("name", "NPC"),
                    "dialogue": tile.properties.get("dialogue", []),
                    "quests": tile.properties.get("quests", [])
                })
        return npcs
        
    def extract_triggers(self, layer):
        triggers = []
        for x, y, tile in layer.tiles():
            if tile:
                triggers.append({
                    "x": x * self.config.TILE_SIZE,
                    "y": y * self.config.TILE_SIZE,
                    "width": self.config.TILE_SIZE,
                    "height": self.config.TILE_SIZE,
                    "type": tile.properties.get("type"),
                    "target_map": tile.properties.get("target_map"),
                    "target_spawn": tile.properties.get("target_spawn")
                })
        return triggers
        
    def load_map(self, map_name):
        if map_name in self.map_data:
            self.current_map = self.map_data[map_name]
            return True
        return False
        
    def get_spawn_point(self, point_type="default"):
        if not self.current_map:
            return None
            
        for point in self.current_map["spawn_points"]:
            if point["type"] == point_type:
                return point
        return None
        
    def check_collision(self, x, y):
        if not self.current_map or not self.current_map["collision_layer"]:
            return False
            
        # 转换世界坐标到瓦片坐标
        tile_x = int(x / self.config.TILE_SIZE)
        tile_y = int(y / self.config.TILE_SIZE)
        
        # 检查是否在地图范围内
        if (tile_x < 0 or tile_x >= self.current_map["tmx"].width or
            tile_y < 0 or tile_y >= self.current_map["tmx"].height):
            return True
            
        # 检查碰撞层
        return bool(self.current_map["collision_layer"].get_tile_gid(tile_x, tile_y))
        
    def check_trigger(self, x, y):
        if not self.current_map:
            return None
            
        for trigger in self.current_map["triggers"]:
            if (trigger["x"] <= x <= trigger["x"] + trigger["width"] and
                trigger["y"] <= y <= trigger["y"] + trigger["height"]):
                return trigger
        return None
        
    def get_npcs(self):
        if not self.current_map:
            return []
        return self.current_map["npcs"]
        
    def render(self, screen, camera):
        if not self.current_map:
            return
            
        # 渲染地图层
        for layer in self.current_map["layers"]:
            for x, y, tile in layer.tiles():
                if tile:
                    screen_x = x * self.config.TILE_SIZE - camera.x
                    screen_y = y * self.config.TILE_SIZE - camera.y
                    screen.blit(tile, (screen_x, screen_y))
                    
    def render_npcs(self, screen, camera):
        if not self.current_map:
            return
            
        for npc in self.current_map["npcs"]:
            screen_x = npc["x"] - camera.x
            screen_y = npc["y"] - camera.y
            # TODO: 渲染NPC精灵
            pygame.draw.circle(screen, (255, 0, 0),
                             (int(screen_x), int(screen_y)), 10) 