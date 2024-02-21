# #### 0. 예제 설명(Introduction)
# Pygame은 쉽게 Game을 제작할 수 있도록 만들어진 module의 집합입니다.
# Python과 제공되는 간단한 몇가지의 함수만을 사용하여 실제로 구동할 수 있는 수준으로 만들 수 있습니다.
# 자세한 사항은 [Pygame Homepage](https://www.pygame.org/)를 참조해주세요.

# 0-1. 사전 준비(prerequirements)
import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])

# #### 1. 모듈 임포트(Module import)
import pygame
import random
import time
from threading import Timer
from InputManager import InputManager
from items.Item import Item

# 1-1. 게임 사전 설정(Settings on the game)

# Frame 수 조절(초당 그려지는 수)
fps = 15

# 창의 크기
frame = (720, 480)

# 색깔 정의 (Red, Green, Blue)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# 시간을 흐르게 하기 위한 FPS counter
fps_controller = pygame.time.Clock()

# 입력을 관리하는 InputManager
inputManager = InputManager(pygame)

# 아이템 리스트
items = []
# 1-2. Pygame 초기화(Initialize Pygame)

def Init(size):
    # 초기화 후 error가 일어났는지 알아봅니다.
    check_errors = pygame.init()

    # pygame.init() example output -> (6, 0)
    # 두번째 항목이 error의 수를 알려줍니다.
    if check_errors[1] > 0:
        print(
            f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')

    # pygame.display를 통해 제목, window size를 설정하고 초기화합니다.
    pygame.display.set_caption('Snake Example with PyGame')
    game_window = pygame.display.set_mode(size)
    return game_window

# ##### 1-3. 기본 logic 함수 모음(basic logics of the game)
# 게임을 플레이하기 위해 필요한 함수들의 모음입니다.
# 자세한 부분은 각 주석을 확인해주세요.

# Score
def show_score(window, size, choice, color, font, fontsize, score, score_growth=0):
    msg = ''
    if choice == 1:
        msg = 'Score : {0} (+{1})'.format(score, score_growth)
    else:
        msg = 'Score : {0}'.format(score)

    # Score를 띄우기 위한 설정입니다.
    # Settings for showing score on screen
    score_font = pygame.font.SysFont(font, fontsize)
    score_surface = score_font.render(msg, True, color)
    score_rect = score_surface.get_rect()

    # Game over 상황인지 게임중 상황인지에 따라 다른 위치를 선정합니다.
    # Select different location depending on the situation.
    if choice == 1:
        score_rect.midtop = (size[0]/8, 15)
    else:
        score_rect.midtop = (size[0]/2, size[1]/1.25)

    # 설정한 글자를 window에 복사합니다.
    # Copy the string to windows
    window.blit(score_surface, score_rect)

def show_stopwatch(window, size, color, font, fontsize, time):
    msg = ''
    time_font = pygame.font.SysFont(font, fontsize)
    time_surface = time_font.render(msg, True, color)
    time_rect = time_surface.get_rect()
    time_rect.midtop = (size[0]/8, 12)

    window.blit(time_surface, time_rect)

# Game Over
def game_over(window, size, score):
    # 'Game Over'문구를 띄우기 위한 설정입니다.
    # Settings of the 'Game Over' string to show on the screen
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (size[0]/2, size[1]/4)

    # window를 검은색으로 칠하고 설정했던 글자를 window에 복사합니다.
    # Fill window as black and copy 'Game Over' strings to main window.
    window.fill(black)
    window.blit(game_over_surface, game_over_rect)

    # 'show_score' 함수를 부릅니다.
    # Call 'show_score' function.
    show_score(window, size, 0, green, 'times', 20, score)

    # 그려진 화면을 실제로 띄워줍니다.
    # Show drawn windows to screen
    pygame.display.flip()

    # 3초 기다린 후 게임을 종료합니다.
    # exit program after 3 seconds.
    time.sleep(3)
    start_game() # 임시

# 스톱워치
class StopWatch(object):
    def __init__(self, interval, score_callback):
        self._timer = None
        self.interval = interval
        self.score_callback = score_callback
        self.is_running = False
        self.start()

    def _run_function(self):
        self.is_running = False
        self.start()
        self.score_callback()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run_function)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


# #### 2. 메인 프로그램
# Game이 동작하기 위한 메인 코드 입니다.

# 초기화
def start_game():
    def update_score():
        nonlocal score
        score += len(snake_body) - 2
        # print("Score updated to:", score)
    
    def gen_item():
        rand = random.randint(1, 6)
        items.append(Item(frame, rand))
        print("생성됨")
        # 아이템 새로 생성하는 코드

    # Game 관련 변수들
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

    food_pos = [random.randrange(1, (frame[0]//10)) * 10,
                random.randrange(1, (frame[1]//10)) * 10]
    food_spawn = True

    direction = 'RIGHT'

    score = 0

    main_window = Init(frame)

    rt = StopWatch(1, update_score)

    itemGenTimer = StopWatch(5, gen_item)

    while True:
        # 게임에서 event를 받아옵니다.
        for event in pygame.event.get():
            # 종료시 실제로 프로그램을 종료합니다.
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                # esc 키를 눌렀을떄 종료 신호를 보냅니다.
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                else:
                    # 입력 키로 방향을 얻어냅니다.
                    direction = inputManager.get_keyboard(event.key, direction)

        # 실제로 뱀의 위치를 옮깁니다.
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # 우선 증가시키고 음식의 위치가 아니라면 마지막을 뺍니다.
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            food_spawn = False
        else:
            snake_body.pop()

        # 음식이 없다면 음식을 랜덤한 위치에 생성합니다.
        if not food_spawn:
            food_pos = [
                random.randrange(1, (frame[0]//10)) * 10,
                random.randrange(1, (frame[1]//10)) * 10
            ]
        food_spawn = True

        # 우선 게임을 검은 색으로 채우고 뱀의 각 위치마다 그림을 그립니다.
        main_window.fill(black)
        for pos in snake_body:
            pygame.draw.rect(main_window, green,
                            pygame.Rect(pos[0], pos[1], 10, 10))

        # 음식을 그립니다.
        pygame.draw.rect(main_window, white,
                        pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        for item in items:
            if item.type == 2:
                item.update_timer(main_window)
            item.draw(main_window)
        # Game Over 상태를 확인합니다.
        # 바깥 벽 처리를 합니다.
        if snake_pos[0] < 0 or snake_pos[0] > frame[0] - 10:
            rt.stop()
            itemGenTimer.stop()

            game_over(main_window, frame, score)
        if snake_pos[1] < 0 or snake_pos[1] > frame[1] - 10:
            rt.stop()
            itemGenTimer.stop()
            game_over(main_window, frame, score)

        # 뱀의 몸에 닿았는지 확인합니다.
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                rt.stop()
                itemGenTimer.stop()
                game_over(main_window, frame, score)

        # 점수를 띄워줍니다.
        score_growth = len(snake_body) - 2
        show_score(main_window, frame, 1, white, 'consolas', 20, score, score_growth)

        # 실제 화면에 보이도록 업데이트 해줍니다.
        pygame.display.update()

        # 해당 FPS만큼 대기합니다.
        fps_controller.tick(fps)

start_game()