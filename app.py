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
import sqlite3

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
        margin_left = 10 
        score_rect.topleft = (margin_left, 15)
    else:
        score_rect.midtop = (size[0]/2, size[1]/1.25)

    # 설정한 글자를 window에 복사합니다.
    # Copy the string to windows
    window.blit(score_surface, score_rect)

def show_stopwatch(window, size, color, font, fontsize, time):
    msg = f'Survive : {convert_seconds_to_min_sec(time)}'
    time_font = pygame.font.SysFont(font, fontsize)
    time_surface = time_font.render(msg, True, color)
    time_rect = time_surface.get_rect()
    
    margin_right = 10
    time_rect.topright = (size[0] - margin_right, 15)
    
    window.blit(time_surface, time_rect)

def convert_seconds_to_min_sec(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"

# Game Over
def game_over(window, size, score, time, length):
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

    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    add_score_query = '''INSERT INTO scoreboard 
    (score, survived_time, snake_length) 
    VALUES ({0}, {1}, {2})'''.format(score, time, length)
    try:
        c.execute(add_score_query)
        conn.commit()
        print('Record inserted successfully')
    except Exception as err:
        print(err)

    conn.close()

    # Button settings
    button_width = 150
    button_height = 50
    button_margin = 20
    
    # Button text and font settings
    button_texts = ["돌아가기", "다시 시작", "게임 종료"]
    FONT_BUTTON = pygame.font.SysFont('Pretendard', 28)

    # Calculate starting position for buttons
    total_button_width = button_width * 3 + button_margin * 2
    start_x = (frame[0] - total_button_width) // 2
    start_y = (frame[1] - button_height) // 2 + 50

    for i, text in enumerate(button_texts):
        button_x = start_x + (button_width + button_margin) * i
        draw_button(text, FONT_BUTTON, (red, green, blue)[i], button_x, start_y, button_width, button_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Define rectangles for each button
                goback_button_rect = pygame.Rect(start_x, start_y, button_width, button_height)
                restart_button_rect = pygame.Rect(start_x + button_width + button_margin, start_y, button_width, button_height)
                finish_button_rect = pygame.Rect(start_x + 2 * (button_width + button_margin), start_y, button_width, button_height)
                # Check if the mouse collides with any button
                if goback_button_rect.collidepoint(mouse_pos):
                    start_screen()
                    return
                elif restart_button_rect.collidepoint(mouse_pos):
                    start_game()
                    return
                elif finish_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


# Keyboard input
def get_keyboard(key, cur_dir):
    # WASD, 방향키를 입력 받으면 해당 방향으로 이동합니다.
    # 방향이 반대방향이면 무시합니다.
    # Chnage direction using WASD or arrow key
    # Ignore keyboard input if input key has opposite direction
    if cur_dir != 'DOWN' and key == pygame.K_UP or key == ord('w'):
        return 'UP'
    if cur_dir != 'UP' and key == pygame.K_DOWN or key == ord('s'):
        return 'DOWN'
    if cur_dir != 'RIGHT' and key == pygame.K_LEFT or key == ord('a'):
        return 'LEFT'
    if cur_dir != 'LEFT' and key == pygame.K_RIGHT or key == ord('d'):
        return 'RIGHT'
    # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
    # Return current direction if none of keyboard input occured
    return cur_dir

# 스톱워치
class StopWatch(object):
    def __init__(self, interval, score_callback):
        self._timer = None
        self.interval = interval
        self.score_callback = score_callback
        self.is_running = False
        self.count_seconds = 0
        self.start()

    def _run_function(self):
        self.is_running = False
        self.count_seconds += 1
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

    # Game 관련 변수들
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    food_pos = [random.randrange(1, (frame[0]//10)) * 10,
                random.randrange(1, (frame[1]//10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    score = 0

    rt = StopWatch(1, update_score)
    bg = pygame.image.load('img/background1.png')

    while True:
        # 게임에서 event를 받아옵니다.
        for event in pygame.event.get():
            # 종료시 실제로 프로그램을 종료합니다.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # esc 키를 눌렀을떄 종료 신호를 보냅니다.
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                else:
                    # 입력 키로 방향을 얻어냅니다.
                    direction = get_keyboard(event.key, direction)

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


        main_window.blit(bg, (0, 0))

        dark = pygame.Surface(frame, flags=pygame.SRCALPHA)
        dark.fill((150, 150, 150, 0))
        main_window.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        for pos in snake_body:
            pygame.draw.rect(main_window, green,
                            pygame.Rect(pos[0], pos[1], 10, 10))

        # 음식을 그립니다.
        pygame.draw.rect(main_window, white,
                        pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        snake_length = len(snake_body) - 2
        # Game Over 상태를 확인합니다.
        # 바깥 벽 처리를 합니다.
        if snake_pos[0] < 0 or snake_pos[0] > frame[0] - 10:
            rt.stop()
            game_over(main_window, frame, score, rt.count_seconds, snake_length)
        if snake_pos[1] < 0 or snake_pos[1] > frame[1] - 10:
            rt.stop()
            game_over(main_window, frame, score, rt.count_seconds, snake_length)

        # 뱀의 몸에 닿았는지 확인합니다.
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                rt.stop()
                game_over(main_window, frame, score, rt.count_seconds, snake_length)

        # 점수를 띄워줍니다.
        score_growth = len(snake_body) - 2
        show_score(main_window, frame, 1, white, 'consolas', 20, score, score_growth)

        show_stopwatch(main_window, frame, white, 'consolas', 20, rt.count_seconds)

        # 실제 화면에 보이도록 업데이트 해줍니다.
        pygame.display.update()

        # 해당 FPS만큼 대기합니다.
        fps_controller.tick(fps)


def start_screen():
    while True:
        main_window.fill(white)

        LOGO = pygame.image.load("img/logo.png")
        FONT_TITLE_PART = pygame.font.SysFont('Pretendard', 16)
        FONT_START_BUTTON = pygame.font.SysFont('Pretendard', 28)
        FONT_DESC_BUTTON = pygame.font.SysFont('Pretendard', 21)

        ico_airplane = pygame.image.load("img/ico_airplane.png")
        resized_ico_airplane = pygame.transform.scale(ico_airplane, (200, 200))
        rotated_ico_airplane = pygame.transform.rotate(resized_ico_airplane, 30)
        ico_bomb = pygame.image.load("img/ico_bomb.png")
        resized_ico_bomb = pygame.transform.scale(ico_bomb, (100, 100))
        rotated_ico_bomb = pygame.transform.rotate(resized_ico_bomb, -30)

        draw_image(LOGO, frame[0] / 2, frame[1] / 10)
        draw_text("폭탄제거로봇", FONT_TITLE_PART, black, frame[0] / 1.7, frame[1] / 2.1)
        draw_image(rotated_ico_airplane, frame[0] / 5, frame[1] / 2.2)
        draw_image(rotated_ico_bomb, frame[0] / 1.2, frame[1] / 2.5)
        draw_button("게임 시작", FONT_START_BUTTON, green, frame[0] / 2 - 70, frame[1] / 1.8, 140, 60)
        draw_button("게임 설명", FONT_DESC_BUTTON, green, frame[0] / 2 - 70, frame[1] / 1.45, 140, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                start_button_rect = pygame.Rect(frame[0] / 2 - 70, frame[1] / 2, 140, 60)
                desc_button_rect = pygame.Rect(frame[0] / 2 - 70, frame[1] / 1.45, 140, 30)
                if start_button_rect.collidepoint(mouse_pos):
                    start_game()
                elif desc_button_rect.collidepoint(mouse_pos):
                    draw_description_screen()
                    return

        pygame.display.flip()

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    main_window.blit(text_surface, text_rect)

def draw_image(image, x, y):
    # Calculate the position to center the image at the top
    image_rect = image.get_rect()
    x_pos = x - image_rect.width / 2
    y_pos = y

    # Draw the image
    main_window.blit(image, (x_pos, y_pos))

def draw_button(text, font, color, x, y, width, height):
    # Draw shadow
    shadow_color = (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30))
    pygame.draw.rect(main_window, shadow_color, (x + 3, y + 3, width, height))
    
    # Draw main button
    pygame.draw.rect(main_window, color, (x, y, width, height))
    
    # Draw text
    draw_text(text, font, black, x + width / 2, y + height / 2)

def draw_description_screen():
    FONT = pygame.font.SysFont('Pretendard', 18)
    TITLE_FONT = pygame.font.SysFont('Pretendard', 50)

    main_window.fill(white)
    draw_text("게임 설명", TITLE_FONT, black, frame[0] // 2, 30)

    draw_text("조작 방법:", FONT, black, frame[0] // 2, 80)

    draw_text("WASD 혹은 방향키를 통하여 뱀이 이동하는 방향을 조정할 수 있습니다.", FONT, black, frame[0] // 2, 120)

    draw_text("아이템 목록:", FONT, black, frame[0] // 2, 160)

    draw_text("1. 상하좌우반전 아이템 (오렌지색):", FONT, black, frame[0] // 2, 200)
    draw_text("- 플레이어의 이동방향이 입력의 반대가 됩니다.", FONT, black, frame[0] // 2, 230)

    draw_text("2. 폭탄 (점멸):", FONT, black, frame[0] // 2, 260)
    draw_text("- 플레이어가 제한시간(15초) 이내에 폭탄에 접근하여 폭탄을 제거해야 합니다.", FONT, black, frame[0] // 2, 290)

    draw_text("3. 속도증감 아이템 (하늘색):", FONT, black, frame[0] // 2, 320)
    draw_text("- 플레이어의 속도를 증가하거나 혹은 감소시킵니다.", FONT, black, frame[0] // 2, 350)

    draw_text("4. 함정 (흰색):", FONT, black, frame[0] // 2, 380)
    draw_text("- 만약 플레이어가 함정에 닿았다면 게임은 끝나게 됩니다.", FONT, black, frame[0] // 2, 410)

    draw_text("5. 길이 증가 아이템 (노란색):", FONT, black, frame[0] // 2, 440)
    draw_text("- 아이템을 먹으면 플레이어의 길이가 1만큼 증가합니다.", FONT, black, frame[0] // 2, 470)

    # Draw back button
    draw_button("돌아가기", FONT, green, 20, 20, 100, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                start_button_rect = pygame.Rect(20, 20, 100, 50)
                if start_button_rect.collidepoint(mouse_pos):
                    start_screen()

        pygame.display.flip()

    pygame.display.update()


if __name__ == "__main__":
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS scoreboard 
                  (trial INTEGER PRIMARY KEY, 
                  score INTEGER DEFAULT NULL, 
                  survived_time INTEGER DEFAULT NULL, 
                  snake_length INTEGER DEFAULT NULL)''')
        print("Table created successfully")
    except Exception as err:
        print(err)

    conn.close()

    main_window = Init(frame)
    start_screen()