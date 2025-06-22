import random


mushroom_weights = [34, 101, 120, 86, 112, 76, 21, 212, 653, 234, 122, 84, 312, 77, 54, 21]

# Initilize
population_count = 20   # Combinations to choose the best solution from
rounds = 34   # Evolutions count
chromosomes = [[random.choice([True, False]) for _ in mushroom_weights]\
                                                    for _ in range(population_count)]


class Weighted:
    max_weight = 1300   # gramms


    def __init__(self, mushroom_weights, chromosome):
        self.chromosome = chromosome
        self.mushrooms_in_bag = [w for w, c in zip(mushroom_weights, chromosome) if c is True]
        self.total_weight = sum(self.mushrooms_in_bag)

        if self.total_weight > self.max_weight:
            self.total_weight = 0


    def __lt__(self, other):
        # rule: less difference between max_weight and total_weight results in higher ranking
        return self.max_weight - self.total_weight < self.max_weight - other.total_weight


for r in range(rounds):
    print(f"=== ROUND {r}, population {len(chromosomes)} ===")
    weighted = [Weighted(mushroom_weights, chromosome) for chromosome in chromosomes]

    # for w in sorted(weighted):
    #     print(w.total_weight)

    # selection
    best = sorted(weighted)[ : 2]
    print(f"Best weight: {best[0].total_weight}")

    # crossover
    offspring = [b.chromosome for b in best]

    for idx in range(int((population_count - 2) / 2)):
        split_index = random.randint(0, len(offspring) - 1)
        c1 = offspring[0][ : split_index] + offspring[1][split_index : ]
        c2 = offspring[1][ : split_index] + offspring[0][split_index : ]

        # mutation
        for idx in range(len(c1)):
            if random.randint(0, 5) == 1:
                c1[idx] = random.choice([True, False])

            if random.randint(0, 5) == 1:
                c2[idx] = random.choice([True, False])

        offspring.append(c1)
        offspring.append(c2)

    chromosomes = offspring
