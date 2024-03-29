import pygame
import random
import items.Color as Color
class Item:
    def __init__(self, frame, type):
        self.position = [random.randrange(1, (frame[0]//10)) * 10,
                             random.randrange(5, (frame[1]//10)) * 10] #[x,y] 위치
        self.type = type # 아이템 종류
        self.spawn_time = pygame.time.get_ticks()
        self.TimeOver = False
        if type==1: #상하좌우반전
            self.color = Color.orange

        if type==2: #폭발
            self.color = Color.red

        if type==3: #속도+
            self.color = Color.skyblue

        if type==4: #속도-
            self.color = Color.skyblue

        if type==5: #함정
            self.color = Color.white

        if type==6: #길이증가
            self.color = Color.yellow

    def update_timer(self, window):

        # 타이머 업데이트 메서드 - 폭탄 아이템이면 app.py에서 실행
        current_time = pygame.time.get_ticks()  # 현재 시간 가져오기
        elapsed_time = current_time - self.spawn_time  # 경과된 시간 계산
        # 깜빡깜빡
        if self.color == Color.red:
            self.color = Color.yellow
        else : self.color = Color.red
        
        if elapsed_time >= 15000:  # 15초 지나면
            #폭발
            self.TimeOver = True

        # 폰트 설정
        font_path = "font/DS-DIGIB.ttf"
        font = pygame.font.Font(font_path, 20)  
        # 텍스트 생성
        if elapsed_time >= 9000: #남은 시간 6초 이하면 빨간색으로 표시
            text = font.render(str((15000 - elapsed_time)/1000) , True, Color.red)
        else: text = font.render(str((15000 - elapsed_time)/1000) , True, Color.white)
        # 텍스트의 위치 설정
        text_rect = text.get_rect()
        text_rect.midbottom = (self.position[0]+5, self.position[1]-5)
        window.blit(text, text_rect)
    
    def draw(self, window):
        pygame.draw.rect(window, self.color,
                         pygame.Rect(self.position[0], self.position[1], 10, 10))
