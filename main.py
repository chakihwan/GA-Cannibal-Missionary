from state import State
from command import CommandList

def print_state(state):
    boat_left = "🚤" if state.boat == 0 else "  "
    boat_right = "🚤" if state.boat == 1 else "  "
    print(f"왼쪽: M{state.left_m} C{state.left_c} {boat_left} | {boat_right} M{state.right_m} C{state.right_c} :오른쪽")

def play_game():
    current_state = State(right_m=3, right_c=3, left_m=0, left_c=0, boat=1)    
    command_list = CommandList()

    print("=== 식인종과 선교사 게임 ===")
    print("목표: 모든 선교사와 식인종을 왼쪽으로 이동시키기")

    while not current_state.goal():
        print("\n현재 상태:")
        print_state(current_state)

        if not command_list.show_commands(current_state):
            print("더 이상 진행할 수 없습니다")
            break

        try:
            user_input = int(input("명령어 번호를 입력하세요 (1-5): "))
            result = command_list.execute_command(user_input, current_state)

            if result == "GAME_OVER":
                print("\n💀 게임 오버!")
                print("선교사가 식인종에게 잡아먹혔습니다!")
                print("규칙: 어느 쪽에서든 선교사 수가 식인종 수보다 적으면 안됩니다.")
                print("(단, 선교사가 0명일 때는 예외)")
                break
            elif result:
                current_state = result
            else:
                print("잘못된 명령어입니다. 다시 시도하세요.")
        
        except ValueError:
            print("1~5 사이의 숫자를 입력해주세요!")
        except KeyboardInterrupt:
            print("\n게임을 종료합니다.")
            break
    
    if current_state.goal():
        print("\n🎉 축하합니다! 모든 선교사와 식인종을 왼쪽으로 이동시켰습니다!")
        print_state(current_state)

if __name__ == "__main__":
    play_game()
    