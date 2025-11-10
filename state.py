class State:
    def __init__(self, right_m, right_c, left_m, left_c, boat):
        self.right_m = right_m
        self.right_c = right_c
        self.left_m = left_m
        self.left_c = left_c
        self.boat = boat

    def is_valid(self):
        # 인원 수 범위 확인
        if (self.right_m < 0 or self.right_c < 0 or
            self.left_m < 0 or self.left_c < 0):
            return False
        
        if (self.right_m > 3 or self.right_c > 3 or
            self.left_m > 3 or self.left_c > 3):
            return False
        
        # 전체 인원 수 확인
        if self.right_m + self.left_m != 3 or self.right_c + self.left_c != 3:
            return False
        
        # 안전 조건 확인 (각 쪽에서 선교사가 식인종보다 적으면 안됨)
        if self.right_m > 0 and self.right_m < self.right_c:
            # print("오른쪽에서 선교사 수가 식인종 수보다 적습니다.")
            return False
        if self.left_m > 0 and self.left_m < self.left_c:
            return False
        
        # 게임 오버 조건도 유효성에 포함
        if self.game_over():
            return False
        
        return True
    

    def goal(self):
        # 목표 상태 모든 선교사와 식인종이 왼쪽에 있어야 함
        return self.left_m == 3 and self.left_c == 3
    
    def game_over(self):
        # 게임 실패 조건
        # 왼쪽에서 선교사가 식인종보다 적고, 선교사가 0명이 아닐 때
        if self.left_m > 0 and self.left_m < self.left_c:
            return True
        
        # 오른쪽에서 선교사가 식인종보다 적고, 선교사가 0명이 아닐 때
        if self.right_m > 0 and self.right_m < self.right_c:
            return True
        
        return False
