import random
from state import State
from command import CommandList

# === 하이퍼파라미터 및 환경 설정 ===
POPULATION_SIZE = 50        # 한 세대의 개체(염색체) 수
MUTATION_RATE = 0.2         # 돌연변이 확률
CHROMOSOME_LENGTH = 11      # 염색체(명령 시퀀스)의 길이, 즉 한 개체가 20번의 action을 가짐

# === 염색체(Chromosome) 클래스 정의 ===
class Chromosome:
    def __init__(self, genes=None):
        if genes is not None:
            # 이미 명령 시퀀스가 주어진 경우 복사
            self.genes = genes.copy()
        else:
            # 새 염색체: 명령 번호(1~5) 중 20개를 무작위로 생성
            self.genes = [random.randint(1, 5) for _ in range(CHROMOSOME_LENGTH)]
        self.fitness = 0    # 적합도 초기화

    def cal_fitness(self):
        # 명령 시퀀스를 실제로 시뮬레이션하여 적합도 평가
        state = State(right_m=3, right_c=3, left_m=0, left_c=0, boat=1)
        cmd_list = CommandList()
        steps = 0
        for cmd_num in self.genes:
            result = cmd_list.execute_command(cmd_num, state)
            if result == "GAME_OVER":
                # 게임 오버(선교사 < 식인종): 큰 패널티
                self.fitness = -100 + steps
                return self.fitness
            elif result is None:
                # 실행 불가 명령: 작은 패널티
                self.fitness -= 10
            else:
                # 정상 이동: 상태 업데이트, 스텝 카운트
                state = result
                steps += 1
            if state.goal():
                # 목표 달성: 높은 점수, 빠를수록 더 높게
                self.fitness = 100 - steps
                return self.fitness
        # 목표 미달성 시 큰 패널티
        self.fitness = -100
        return self.fitness

    def __str__(self):
        return f"{self.genes}"

# === 선택 연산: 룰렛휠 방식 ===
def select(pop):
    max_value = sum([c.cal_fitness() for c in pop])
    if max_value <= 0:
        # 모든 적합도가 0 이하인 경우, 랜덤으로 선택
        return random.choice(pop)
    pick = random.uniform(0, max_value)
    current = 0
    for c in pop:
        current += c.cal_fitness()
        if current > pick:
            return c

# === 교차 연산: 단일점 교차 ===
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index = random.randint(1, CHROMOSOME_LENGTH - 1)
    # 부모의 명령 시퀀스를 교차점에서 섞어 자식 2명 생성
    child1 = father.genes[:index] + mother.genes[index:]
    child2 = mother.genes[:index] + father.genes[index:]
    return (child1, child2)

# === 돌연변이 연산: 명령 하나를 무작위로 변경 ===
def mutate(c):
    for i in range(CHROMOSOME_LENGTH):
        if random.random() < MUTATION_RATE:
            c.genes[i] = random.randint(1, 5)

# === 개체군(세대) 상태 출력 ===
def print_p(pop):
    i = 0
    for x in pop:
        print("염색체 #", i, "=", x, "적합도=", x.cal_fitness())
        i += 1
    print("")

# === 메인 루프: 유전자 알고리즘의 전체 흐름 ===

# 1. 초기 개체군 생성 (랜덤 명령 시퀀스)
population = [Chromosome() for _ in range(POPULATION_SIZE)]
count = 0

# 2. 초기 세대 출력
population.sort(key=lambda x: x.cal_fitness(), reverse=True)
print("세대 번호=", count)
print_p(population)
count = 1

# 3. 세대 반복
while population[0].cal_fitness() < 80:  # 100점 만점, 80 이상이면 성공(목표 도달)
    new_pop = []
    # 4. 교차 연산을 통해 자식 생성
    for _ in range(POPULATION_SIZE // 2):
        c1, c2 = crossover(population)
        new_pop.append(Chromosome(c1))
        new_pop.append(Chromosome(c2))
    # 5. 자식 세대로 교체
    population = new_pop.copy()
    # 6. 돌연변이 연산 적용
    for c in population:
        mutate(c)
    # 7. 적합도 기준 정렬 및 출력
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    print("세대 번호=", count)
    print_p(population)
    count += 1

print("=== 최종 세대 전체 유전자 ===")
print("세대 번호=", count - 1)
print_p(population)
    # 8. 반복 제한(옵션)
    # if count > 200: break

# === 요약 설명 ===
# - 각 염색체는 20개의 명령 시퀀스로 구성되어, 자동으로 게임을 플레이함
# - 적합도는 목표 달성 여부, 스텝 수, 게임 오버 여부를 반영
# - 교차와 돌연변이 하이퍼파라미터로 진화의 다양성 확보
# - 세대가 반복될수록 더 우수한 명령 시퀀스(즉, 자동화된 해답)를 찾아감