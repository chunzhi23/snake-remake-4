import random

class ItemGenerator:
    def __init__(self):
        self.item_list = [] #클래스 or 함수 넣기
    
    def gen(self, pos):
        length = len(self.item_list)
        randInt = random.randint(0, length)
        selectItem = self.item_list[randInt]
        # 아이템 랜덤하게 선택 후 함수 실행. pos는 좌표값.
