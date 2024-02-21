class InputManager:
    def __init__(self, pygame):
        self.pygame = pygame
        self.reverse = False

    def init(self):
        self.reverse = False

    def get_default_direction(self):
        self.reverse = False
        return "RIGHT"

    def on_reverse(self):
        if self.reverse:
            self.reverse = False
        else:
            self.reverse = True
    
        # Keyboard input
    def get_keyboard(self, key, cur_dir):
        # WASD, 방향키를 입력 받으면 해당 방향으로 이동합니다.
        # 방향이 반대방향이면 무시합니다.
        # Chnage direction using WASD or arrow key
        # Ignore keyboard input if input key has opposite direction
        if not self.reverse:
            if (cur_dir != 'DOWN') and (key == self.pygame.K_UP or key == ord('w')):
                return 'UP'
            if (cur_dir != 'UP') and (key == self.pygame.K_DOWN or key == ord('s')):
                return 'DOWN'
            if (cur_dir != 'RIGHT') and (key == self.pygame.K_LEFT or key == ord('a')):
                return 'LEFT'
            if (cur_dir != 'LEFT') and (key == self.pygame.K_RIGHT or key == ord('d')):
                return 'RIGHT'
            # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
            # Return current direction if none of keyboard input occured
            return cur_dir
        else:
            if (cur_dir != 'UP') and (key == self.pygame.K_UP or key == ord('w')):
                return 'DOWN'
            if (cur_dir != 'DOWN') and (key == self.pygame.K_DOWN or key == ord('s')):
                return 'UP'
            if (cur_dir != 'LEFT') and (key == self.pygame.K_LEFT or key == ord('a')):
                return 'RIGHT'
            if (cur_dir != 'RIGHT') and (key == self.pygame.K_RIGHT or key == ord('d')):
                return 'LEFT'
            # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
            # Return current direction if none of keyboard input occured
            return cur_dir