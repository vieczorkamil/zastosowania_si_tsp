import random
import copy


class GeneticAlgorithm:
    def __init__(self, population_size, crossover_probability, mutation_probability, iterations, dataset_file, tournament_size):
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.iterations = iterations
        self.dataset_file = dataset_file
        self.tournament_size = tournament_size
        self.distances = self.load_distances(self.dataset_file)
        self.path_size = len(self.distances)


    def load_distances(self, path: str) -> list[list[int]]:
        distances = []
        i = 0
        with open(path) as f:
            for line in f.readlines():
                if i == 0:
                    i += 1
                    continue
                distances.append([int(x) for x in line.strip().split(" ")])
        for i, row in enumerate(distances):
            for other_row in distances[i+1:]:
                row.append(other_row[i])
        return distances


    def generate_population(self) -> list[list[int]]:
        return [self.get_random_path(self.path_size) for _ in range(self.population_size)]
    
    
    def get_random_path(self, size: int) -> list[int]:
        path = [i for i in range(size)]
        random.shuffle(path)
        return path


    def calculate_distance(self, path: list[int]) -> int:
        distance = 0
        path_length = len(path)
        for i, city in enumerate(path):
            tmp = self.distances[city][path[(i + 1) % path_length]]
            distance += tmp
        return distance


    def tournament_selection(self, population: list[list[int]]) -> list[list[int]]:
        new_population = []
        for _ in range(len(population)):
            selected_population = random.choices(population, k=self.tournament_size)
            new_population.append(self.get_best_from_population(selected_population))
        return new_population


    def get_best_from_population(self, population: list[list[int]]) -> list[int]:
        best = None
        best_distance = None
        for path in population:
            if best == None:
                best = path
                best_distance = self.calculate_distance(path)
            elif self.calculate_distance(path) < best_distance:
                best = path
                best_distance = self.calculate_distance(path)
        return best


    # FIXME: 
    def pmx_crossover(self, probability: float, population: list[list[int]]) -> list[list[int]]:
        new_population = []
        for i in range(0, len(population), 2):
            try:
                parent1 = population[i]
                parent2 = population[i + 1]
            except IndexError:
                new_population.append(parent1)
                continue

            if random.random() > probability:
                new_population.append(parent1)
                new_population.append(parent2)
                continue

            crossover_point1 = random.randint(0, len(parent1) - 2)
            crossover_point2 = random.randint(crossover_point1 + 1, len(parent1) - 1)

            child1, child2 = parent1[:], parent2[:]

            # Create mapping between parents
            mapping = {parent1[i]: parent2[i] for i in range(crossover_point1, crossover_point2)}
            for i in range(len(child1)):
                if crossover_point1 <= i < crossover_point2:
                    continue
                while child1[i] in mapping:
                    child1[i] = mapping[child1[i]]

            mapping = {parent2[i]: parent1[i] for i in range(crossover_point1, crossover_point2)}
            for i in range(len(child2)):
                if crossover_point1 <= i < crossover_point2:
                    continue
                while child2[i] in mapping:
                    child2[i] = mapping[child2[i]]

            new_population.append(child1)
            new_population.append(child2)

        return new_population


    def swap_mutation(self, probability: float, population: list[list[int]]) -> list[list[int]]:
        for path in population:
            if random.random() < probability:
                x1 = random.randint(0, len(path) - 2)
                x2 = random.randint(x1, len(path) - 1)
                path[x1:x2] = path[x1:x2][::-1]
        return population
    

    def get_n_best(self, population: list[list[int]], n: int) -> list[list[int]]:
        scores = []
        for path in population:
            scores.append((path, self.calculate_distance(path)))
        scores.sort(key=lambda x: x[1])
        new_population = []
        for i in range(n):
            new_population.append(scores[i][0])
        return new_population


    def partial_replacement_succession(self, old_population: list[list[int]], new_population: list[list[int]], ratio: float) -> list[list[int]]:
        from_new = int(len(new_population) * ratio)
        from_old = len(new_population) - from_new
        return self.get_n_best(new_population, from_new) + self.get_n_best(old_population, from_old)


    def run_genetic_algorithm(self):
        stagnation_iteration = 0
        try:
            population = self.generate_population()
            __crossover_probability = self.crossover_probability
            __mutation_probability = self.mutation_probability
            previous_best_distance = None
            for iteration in range(self.iterations):
                if stagnation_iteration >= 1000:
                    __mutation_probability = random.uniform(0.7, 0.99)
                    __crossover_probability = random.uniform(0.2, 0.4)
                    stagnation_iteration = 0
                old_pop = copy.deepcopy(population)
                population = self.tournament_selection(population)
                population = self.pmx_crossover(__crossover_probability, population)
                population = self.swap_mutation(__mutation_probability, population)
                population = self.partial_replacement_succession(old_pop, population, 0.75)
                best_path = self.get_best_from_population(population)
                best_distance = self.calculate_distance(best_path)
                if best_distance == previous_best_distance:
                    stagnation_iteration += 1
                else:
                    previous_best_distance = best_distance
                    __crossover_probability = self.crossover_probability
                    __mutation_probability = self.mutation_probability
                    stagnation_iteration = 0
                print(f"Iteration: {iteration}", end="\r")
        except KeyboardInterrupt:
            print(f"Break at iteration num: {iteration}")
        finally:
            print("------------------------------------------------------")
            print(f"Best path found: {best_path}")
            print(f"The distance was: {best_distance}")
            print(len(best_path), len(best_path) == len(set(best_path)))
            print("------------------------------------------------------")


