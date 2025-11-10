import random
from state import State
from command import CommandList

# === 하이퍼파라미터 및 환경 설정 ===
POPULATION_SIZE = 50        # 한 세대의 개체(염색체) 수
MUTATION_RATE = 0.2         # 돌연변이 확률
CHROMOSOME_LENGTH = 20      # 염색체의 길이
ELITE_SIZE = 1  # 보존할 엘리트 개수

# === 염색체 클래스 ===
class Chromosome:
    def __init__(self, genes=None):
        if genes is not None:
            self.genes = genes.copy()
        else:
            self.genes = [random.randint(1, 5) for _ in range(CHROMOSOME_LENGTH)]
        self.fitness = 0

    def cal_fitness(self):
        state = State(right_m=3, right_c=3, left_m=0, left_c=0, boat=1)
        cmd_list = CommandList()
        steps = 0
        self.fitness = 0  # 초기화

        for cmd_num in self.genes:
            result = cmd_list.execute_command(cmd_num, state)
            if result == "GAME_OVER":
                self.fitness = -100 + steps
                return self.fitness
            elif result is None:
                self.fitness -= 10
            else:
                state = result
                steps += 1
            if state.goal():
                self.fitness = 100 - steps
                return self.fitness

        self.fitness = -100
        return self.fitness

    def __str__(self):
        return f"{self.genes}"

# === 선택 연산 (룰렛휠 방식) ===
def select(pop):
    total_fitness = sum([c.cal_fitness() for c in pop])
    if total_fitness <= 0:
        return random.choice(pop)
    pick = random.uniform(0, total_fitness)
    current = 0
    for c in pop:
        current += c.cal_fitness()
        if current > pick:
            return c

# === 교차 연산 (단일점 교차) ===
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index = random.randint(1, CHROMOSOME_LENGTH - 1)
    child1 = father.genes[:index] + mother.genes[index:]
    child2 = mother.genes[:index] + father.genes[index:]
    return (child1, child2)

# === 돌연변이 연산 ===
def mutate(c):
    for i in range(CHROMOSOME_LENGTH):
        if random.random() < MUTATION_RATE:
            c.genes[i] = random.randint(1, 5)

# === 개체 정보 출력 ===
def print_p(pop):
    for i, x in enumerate(pop):
        print("염색체 #", i, "=", x, "적합도=", x.cal_fitness())
    print("")

# === 메인 루프 ===
population = [Chromosome() for _ in range(POPULATION_SIZE)]
count = 0

# 초기 세대 정렬 및 출력
population.sort(key=lambda x: x.cal_fitness(), reverse=True)
print("세대 번호 =", count)
print_p(population)
count += 1

while population[0].cal_fitness() < 80:
    new_pop = []
    # 1. 엘리트 복사
    elites = population[:ELITE_SIZE]
    for elite in elites:
        new_pop.append(Chromosome(elite.genes))
    # 2. 교차 연산을 통해 자식 생성 (엘리트 제외)
    for _ in range((POPULATION_SIZE - ELITE_SIZE) // 2):
        c1, c2 = crossover(population)
        new_pop.append(Chromosome(c1))
        new_pop.append(Chromosome(c2))
    # 3. 자식 세대로 교체
    population = new_pop.copy()
    # 4. 돌연변이 연산 적용
    for c in population[ELITE_SIZE:]:  # 엘리트는 돌연변이 제외
        mutate(c)
    # 5. 적합도 기준 정렬 및 출력
    population.sort(key=lambda x: x.cal_fitness(), reverse=True)
    print("세대 번호=", count)
    print_p(population)
    count += 1