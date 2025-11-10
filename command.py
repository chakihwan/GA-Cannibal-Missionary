from state import State

class Command:
    def __init__(self, command_num, missionaries, cannibals, description):
        self.command_num = command_num
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.description = description
    
    def execute(self, current_state):
        if not self.can_execute(current_state):
            return None
        
        # 보트가 왼쪽에 있을 때 
        # 왼쪽에서 오른쪽으로 이동
        if current_state.boat == 0:
            new_state = State(
                right_m=current_state.right_m + self.missionaries,
                right_c=current_state.right_c + self.cannibals,
                left_m=current_state.left_m - self.missionaries,
                left_c=current_state.left_c - self.cannibals,
                boat = 1
                )
            
        # 보트가 오른쪽에 있을 때 
        # 오른쪽에서 왼쪽으로 이동
        else:
            new_state = State(
                right_m=current_state.right_m - self.missionaries,
                right_c=current_state.right_c - self.cannibals,
                left_m=current_state.left_m + self.missionaries,
                left_c=current_state.left_c + self.cannibals,
                boat = 0
                )
        # 게임 오버 상태면 "GAME_OVER" 반환
        if not new_state.is_valid():
            return "GAME_OVER"
        
        return new_state
    
    def can_execute(self, current_state):
    # 현재 상태에서 이 명령을 실행할 수 있는지 확인
        if current_state.boat == 1:  # 오른쪽에서 출발
            return (current_state.right_m >= self.missionaries and 
                    current_state.right_c >= self.cannibals)
        else:  # 왼쪽에서 출발
            return (current_state.left_m >= self.missionaries and 
                    current_state.left_c >= self.cannibals)

    
    def __str__(self):
        return f"{self.command_num}: {self.description} (M: {self.missionaries}, C: {self.cannibals})"

class CommandList:
    def __init__(self):
        self.commands = {
            1: Command(1, 1, 0, "선교사 1명 이동"),
            2: Command(2, 2, 0, "선교사 2명 이동"),
            3: Command(3, 1, 1, "선교사 1명 ,식인종 1명 이동"),
            4: Command(4, 0, 1, "식인종 1명 이동"),
            5: Command(5, 0, 2, "식인종 2명 이동")
        }
    
    def get_command(self, command_num):
        return self.commands.get(command_num)
    
    def show_commands(self, current_state):
        print("가능한 명령어:")
        available = False

        for cmd_num, command in self.commands.items():
            can_execute =  command.can_execute(current_state)
            # print(f"명령 {cmd_num}: {command.description} - 실행가능: {can_execute}")
            if can_execute:
                print(f"{command}")
                available = True

        if not available:
            print("가능한 명령어가 없습니다.")
            
        return available

    def execute_command(self, command_num, current_state):
        command = self.get_command(command_num)
        
        if command is None:
            # print(f"명령어 {command_num}은(는) 존재하지 않습니다.")
            return None
        
        if not command.can_execute(current_state):
            # print(f"명령어 {command_num}은(는) 현재 상태에서 실행할 수 없습니다.")
            return None
        
        new_state = command.execute(current_state)

        if new_state is None:
            # print(f"{command.description} 실행 후 상태가 유효하지 않습니다.")
            return None
        
        # print(f"{command.description} 명령을 실행했습니다.")
        return new_state