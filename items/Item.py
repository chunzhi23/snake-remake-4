import pygame
import random
import Color
class Item:
    def __init__(self, frame, type):
        self.position = [random.randrange(1, (frame[0]//10)) * 10,
                             random.randrange(1, (frame[1]//10)) * 10] #[x,y] 위치
        self.type = type # 아이템 종류
        self.spawn_time = pygame.time.get_ticks()
        
        if type==1: #상하좌우반전
            self.color = Color.orange

        if type==2: #폭발
            self.color = Color.red

        if type==3: #속도+
            self.color = Color.skyblue

        if type==4: #속도-
            self.color = Color.skyblue

        if type==5: #함정
            self.color = Color.black

        if type==6: #길이증가
            self.color = Color.yellow

    def update_timer(self):
        # 타이머 업데이트 메서드 - 폭탄 아이템이면 app.py에서 실행
        current_time = pygame.time.get_ticks()  # 현재 시간 가져오기
        elapsed_time = current_time - self.spawn_time  # 경과된 시간 계산
        
        if elapsed_time >= 5000:  # 30초 지나면
            #폭발
            print("폭발함")
    
    def draw(self, window):
        pygame.draw.rect(window, self.color,
                         pygame.Rect(self.position[0], self.position[1], 10, 10))

    