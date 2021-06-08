from functools import partial
from random import choice, randint, choices, random
from typing import List, Callable, Tuple, Optional
from fitness import bias

# Defining Type
RoomCell = List[int]  # 0~14=種類one-hot; (15,16)=方向
RoomMap = List[List[RoomCell]]
Population = List[RoomMap]

# Functions
# FitnessFunc = Callable[[RoomMap], int]  # fitness_adapter
# PopulateFunc = Callable[[int, int, int, float], Population]  # random_population
# SelectionFunc = Callable[[Population, FitnessFunc], Population]  # select_parents_pair
# CrossoverFunc = Callable[[RoomMap, RoomMap], Tuple[RoomMap, RoomMap]]  # single_point_crossover
# MutationFunc = Callable[[RoomMap, Optional[float]], None]  # mutation

# Constants & Mapping
orientations = [
    [0, 1],  # N
    [0, -1],  # S
    [1, 0],  # E
    [-1, 0],  # W
]
id_to_mapitemname = {
    0: 'Whiteboard',
    1: 'Projector Screen',
    2: 'Chippendale Table (2x3)',
    3: 'TV (Flatscreen)',
    4: 'Bookshelf (2x4)',
    5: 'Potted Plant (Spikey)',
    6: 'Mod Chair',
    7: 'Captain’s Chair',
    8: 'Chair (Simple)',
    9: 'Chippendale Table (3x3)',
    10: 'Bookshelf [Tall] (1x2)',
    11: 'Laptop',
    12: 'Microphone',
    13: 'Lucky Bamboo',
    14: 'Dining Chair (Square)'
}
W = 10
H = 13
P = 0.5
M_P = 0.05
FITNESS_LIMIT = 10
P_SIZE = 10


def one_hot_mapitem(prob: float) -> RoomCell:
    arr = [0] * len(id_to_mapitemname)
    if random() > prob:
        arr.extend([0, 0])
        return arr
    arr[randint(0, len(id_to_mapitemname) - 1)] = 1
    arr.extend(choice(orientations))
    return arr


def random_room_map(w: int = W, h: int = H, prob: float = P) -> RoomMap:
    return [[one_hot_mapitem(prob) for _ in range(w)] for _ in range(h)]


def random_population(size: int, w: int = W, h: int = H, prob: float = P) -> Population:
    return [random_room_map(w, h, prob) for _ in range(size)]


def fitness(room_map: RoomMap, limit: int = 5000) -> int:
    value = 0
    weight = 0

    for i in range(H):
        for j in range(W):
            for hot in range(len(id_to_mapitemname)):
                if room_map[i][j][hot] == 1:
                    v, w = bias.fitness(hot, room_map, i, j)
                    value += v
                    weight += w
                    break
    if weight > limit:
        return 0
    return value


def fitness_adapter(room_map: RoomMap) -> int:
    return fitness(room_map)  # (W,H)=global, limit=default


def select_parents_pair(p: Population, fitness_func) -> Population:
    # print(f"debug---p={p}")
    # print(f"debug---select_parents_pair, weights={[fitness_func(room_map) for room_map in p]}")
    return choices(
        population=p,
        weights=[fitness_func(room_map) for room_map in p],
        k=2
    )


def single_point_crossover(a: RoomMap, b: RoomMap) -> Tuple[RoomMap, RoomMap]:
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("RoomMap should have the same (w, h)")
    new_a = a
    new_b = b
    new_a[H//2:], new_b[H//2:] = new_a[H//2:], new_b[H//2:]
    for i in range(H):
        new_a[i][W//2:], new_b[i][W//2:] = new_b[i][W//2:], new_a[i][W//2:]
    return new_a, new_b


def mutation(room_map: RoomMap, prob: Optional[float] = M_P) -> None:
    if random() > 0.05:
        return
    ri = randint(0, H-1)
    rj = randint(0, W-1)
    room_map[ri][rj] = one_hot_mapitem(prob)


def run_evo(
        populate_func,
        fitness_func,
        fitness_limit: int,
        selection_func,
        crossover_func,
        mutation_func,
        generation_limit: int) -> Tuple[Population, int]:

    population = populate_func(P_SIZE)

    i = 0
    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda room_map: fitness_func(room_map),
            reverse=True
        )

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[:2]  # pick elites first

        for j in range(len(population)):
            parents = selection_func(population, fitness_func)
            c1, c2 = crossover_func(parents[0], parents[1])
            mutation_func(c1)
            mutation_func(c2)
            next_generation.extend([c1, c2])

        population = next_generation

    population = sorted(
        population,
        key=lambda room_map: fitness_func(room_map),
        reverse=True
    )

    return population, i


if __name__ == '__main__':

    population, gens = run_evo(
        populate_func=random_population,
        fitness_func=fitness_adapter,
        fitness_limit=FITNESS_LIMIT,
        selection_func=select_parents_pair,
        crossover_func=single_point_crossover,
        mutation_func=mutation,
        generation_limit=100
    )

    print(f"------------population------------:\n{population}")
    print(f"------------generation------------:\n{gens}")




