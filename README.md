# 식인종-선교사 문제 유전자 알고리즘 (GA)

이 프로젝트는 고전적인 AI 탐색 문제인 **'식인종-선교사 강 건너기 문제'**를 **유전자 알고리즘(Genetic Algorithm)**을 사용하여 해결합니다.

이 구현의 목표는 **오른쪽 강둑(Right Bank)**에 있는 3명의 선교사와 3명의 식인종을 2인용 배 한 척으로 **왼쪽 강둑(Left Bank)**으로 모두 이동시키는 최적의 '행동 순서'를 찾는 것입니다.



---

## 1. 프로젝트 파일 구조 및 역할

이 프로젝트는 '게임 환경'을 정의하는 파일들과 '해를 찾는 솔버'로 구성됩니다.

### 1. 게임 환경 (Game Engine)

* **`state.py`**:
    * `State` 클래스를 통해 현재 강 양쪽의 인원과 배의 위치(`boat=1`은 오른쪽)를 정의합니다.
    * `is_valid()`: **핵심 규칙**이 구현된 함수입니다. 이동 후의 상태가 유효한지(인원수, 음수 값, 그리고 **"선교사가 잡아먹히는"** 조건)를 판별합니다.
    * `goal()`: `left_m == 3 and left_c == 3` (왼쪽 강둑에 모두 도착)인지 확인하는 성공 조건 함수입니다.

* **`command.py`**:
    * `Command` 클래스로 5가지 행동(예: "선교사 1명 이동")을 정의합니다.
    * `CommandList` 클래스의 `execute_command` 함수가 GA의 핵심 인터페이스 역할을 합니다.
    * 이 함수는 행동 실행 전 `can_execute` (인원이 충분한지)를 확인합니다.
    * 행동 실행 후, `new_state.is_valid()`를 호출하여 **새 상태가 유효한지(선교사가 안전한지) 검사**합니다. 만약 `is_valid()`가 `False`를 반환하면, GA에게 **`"GAME_OVER"`** 문자열을 반환합니다.

### 2. GA 솔버 (Solver - 해 찾기)

* **`eliteGenetic.py`**:
    * 이 프로젝트의 **메인 솔버(Solver)** 스크립트입니다.
    * **엘리트주의(Elitism)**와 **룰렛 휠 선택(Roulette Wheel Selection)**을 사용하여 최적의 해(염색체)를 탐색합니다.

---

## 2. 알고리즘 핵심 구현 (`eliteGenetic.py`)

* **염색체 (Chromosome)**:
    * `CHROMOSOME_LENGTH = 20`으로 설정된 '행동 순서(1~5)의 리스트'입니다.

* **적합도 함수 (Fitness Function)**:
    * `cal_fitness` 함수는 염색체(행동 순서)를 `command.py`와 `state.py`를 이용해 시뮬레이션합니다.
    * **시작 상태**: `State(right_m=3, right_c=3, ... boat=1)` (모두 오른쪽에 있음)
    * **성공 (보상)**: `state.goal()`에 성공하면 `100 - steps` 점을 부여합니다. (즉, 더 짧은 단계로 성공할수록 적합도가 높습니다.)
    * **실패 (페널티)**:
        * `result == "GAME_OVER"` (즉, `state.is_valid()`가 `False` 반환): `-100 + steps` 점을 부여합니다.
        * `result is None` (유효하지 않은 행동, 예: `can_execute` 실패): `fitness -= 10` 페널티를 부여합니다.
        * `Time Over` (20단계 내 성공 못함): `-100` 점을 부여합니다.

* **진화 (Evolution)**:
    * **선택 (Selection)**: **룰렛 휠 선택**을 사용합니다. (`select` 함수) 적합도가 음수일 경우를 대비해 예외 처리가 되어있습니다.
    * **교차 (Crossover)**: **단일점 교차**를 사용합니다. (`crossover` 함수)
    * **엘리트주의 (Elitism)**:
        * `ELITE_SIZE = 1`로 설정되어, 매 세대마다 가장 적합도가 높은 **최우수 해 1개**를 다음 세대로 **그대로 보존**합니다.
        * 이 엘리트 개체는 **돌연변이 연산에서 제외**되어 안정적으로 우수 유전자를 보존합니다.

---

## 3. 실행 결과 (솔버 & 테스터)

`eliteGenetic.py` (솔버)를 실행하여 최적의 해(커맨드 리스트)를 찾고, 이 해를 검증용 스크립트(예: `main.py`)에 입력하여 최종 성공을 확인합니다.

| 1. 솔버 실행 결과 (최적해 발견) | 2. 테스터 실행 결과 (해답 검증) |
| :---: | :---: |
| `eliteGenetic.py`가 찾은 최적해(염색체)와 적합도. (예: `80` 이상) | 위에서 찾은 해를 검증용 스크립트에 입력하여 실행한 최종 결과. |
| <img width="407" height="558" alt="image" src="https://github.com/user-attachments/assets/abc5d996-fea0-4d20-b1a3-f7dddc2749e6" /> | <img width="442" height="891" alt="image" src="https://github.com/user-attachments/assets/bcc1ad04-2027-4103-83be-f675286d5a80" /> |
---

## 4. 실행 방법 및 워크플로우

1.  **[1단계] 최적의 해 찾기 (Solver 실행)**
    `eliteGenetic.py`를 실행하여 최적의 해(염색체 리스트)를 찾습니다.

    ```bash
    python eliteGenetic.py
    ```

2.  **[2단계] 해답(염색체) 복사**
    콘솔에 `염색체 #0 = [5, 1, 3, 2, ...]`와 같이 가장 높은 적합도의 해가 출력되면, 이 리스트를 복사합니다.

3.  **[3단계] 해답 검증 (Tester 실행)**
    1.  `main.py`(솔루션 검증용 스크립트) 파일을 엽니다. 
    2.  `main.py`를 실행하여 이 해답이 문제를 올바르게 해결하는지 단계별로 확인합니다.

    ```bash
    python main.py
    ```
