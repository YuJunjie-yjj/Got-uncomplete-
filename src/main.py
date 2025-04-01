import pygame
import sys
from config import Config
from core.game import Game

def main():
    # 初始化Pygame
    pygame.init()
    
    # 创建配置对象
    config = Config()
    
    try:
        # 创建游戏实例
        game = Game(config)
        
        # 运行游戏
        game.run()
        
    except Exception as e:
        print(f"游戏发生错误: {e}")
        pygame.quit()
        sys.exit(1)
        
    finally:
        # 确保正确退出
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main() 