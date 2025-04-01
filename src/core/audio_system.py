import pygame
import os
import random

class AudioSystem:
    def __init__(self, config):
        self.config = config
        self.sounds = {}
        self.music = {}
        self.current_music = None
        self.volume = 1.0
        self.music_volume = 0.5
        self.load_audio()
        
    def load_audio(self):
        # 初始化pygame音频系统
        pygame.mixer.init()
        
        # 加载音效
        sounds_dir = "assets/audio/sounds"
        for filename in os.listdir(sounds_dir):
            if filename.endswith('.wav'):
                sound_name = os.path.splitext(filename)[0]
                sound_path = os.path.join(sounds_dir, filename)
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                
        # 加载音乐
        music_dir = "assets/audio/music"
        for filename in os.listdir(music_dir):
            if filename.endswith('.mp3'):
                music_name = os.path.splitext(filename)[0]
                music_path = os.path.join(music_dir, filename)
                self.music[music_name] = music_path
                
    def play_sound(self, sound_name, volume=1.0):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume * self.volume)
            self.sounds[sound_name].play()
            
    def play_music(self, music_name, fade_in=1000):
        if music_name in self.music:
            # 如果当前正在播放音乐，先停止
            if self.current_music:
                pygame.mixer.music.fadeout(fade_in)
                
            # 播放新音乐
            pygame.mixer.music.load(self.music[music_name])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # -1表示循环播放
            self.current_music = music_name
            
    def stop_music(self, fade_out=1000):
        if self.current_music:
            pygame.mixer.music.fadeout(fade_out)
            self.current_music = None
            
    def pause_music(self):
        if self.current_music:
            pygame.mixer.music.pause()
            
    def resume_music(self):
        if self.current_music:
            pygame.mixer.music.unpause()
            
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
            
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        if self.current_music:
            pygame.mixer.music.set_volume(self.music_volume)
            
    def play_ambient_sounds(self, location_type):
        # 根据位置类型播放环境音效
        if location_type == "forest":
            self.play_sound("wind", 0.3)
            self.play_sound("birds", 0.2)
        elif location_type == "castle":
            self.play_sound("torch", 0.2)
            self.play_sound("footsteps", 0.1)
        elif location_type == "battlefield":
            self.play_sound("battle_ambient", 0.4)
            
    def play_combat_sounds(self, action_type):
        # 播放战斗音效
        if action_type == "sword_swing":
            self.play_sound("sword_swing", 0.8)
        elif action_type == "arrow_shoot":
            self.play_sound("arrow_shoot", 0.7)
        elif action_type == "spell_cast":
            self.play_sound("spell_cast", 0.9)
        elif action_type == "hit":
            self.play_sound("hit", 0.6)
            
    def play_dialogue_sounds(self, character_type):
        # 播放对话音效
        if character_type == "noble":
            self.play_sound("noble_voice", 0.5)
        elif character_type == "peasant":
            self.play_sound("peasant_voice", 0.5)
        elif character_type == "warrior":
            self.play_sound("warrior_voice", 0.5)
            
    def play_weather_sounds(self, weather_type):
        # 播放天气音效
        if weather_type == "rain":
            self.play_sound("rain", 0.4)
        elif weather_type == "thunder":
            self.play_sound("thunder", 0.8)
        elif weather_type == "wind":
            self.play_sound("wind", 0.3)
            
    def play_quest_sounds(self, event_type):
        # 播放任务相关音效
        if event_type == "quest_complete":
            self.play_sound("quest_complete", 0.7)
        elif event_type == "quest_fail":
            self.play_sound("quest_fail", 0.7)
        elif event_type == "quest_update":
            self.play_sound("quest_update", 0.5) 