class InputManager:
    def __init__(self, pygame):
        self.direction = "RIGHT"
        self.pygame = pygame
        self.reverse = False

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
            if self.direction != 'DOWN' and key == self.pygame.K_UP or key == ord('w'):
                self.direction = "UP"
                return 'UP'
            if self.direction != 'UP' and key == self.pygame.K_DOWN or key == ord('s'):
                self.direction = "DOWN"
                return 'DOWN'
            if self.direction != 'RIGHT' and key == self.pygame.K_LEFT or key == ord('a'):
                self.direction = "LEFT"
                return 'LEFT'
            if self.direction != 'LEFT' and key == self.pygame.K_RIGHT or key == ord('d'):
                self.direction = "RIGHT"
                return 'RIGHT'
            # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
            # Return current direction if none of keyboard input occured
            return cur_dir
        else:
            if self.direction != 'UP' and (key == self.pygame.K_UP or key == ord('w')):
                self.direction = "DOWN"
                return 'DOWN'
            if self.direction != 'DOWN' and (key == self.pygame.K_DOWN or key == ord('s')):
                self.direction = "UP"
                return 'UP'
            if self.direction != 'LEFT' and (key == self.pygame.K_LEFT or key == ord('a')):
                self.direction = "RIGHT"
                return 'RIGHT'
            if self.direction != 'RIGHT' and (key == self.pygame.K_RIGHT or key == ord('d')):
                self.direction = "LEFT"
                return 'LEFT'
            # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
            # Return current direction if none of keyboard input occured
            return cur_dir