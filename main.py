import argparse
import random


class GeneticAlgorithm:
    def __init__(self, population_size: int, crossover_probability: float, 
                 mutation_swap_probability: float, mutation_inversion_probability: float, 
                 iterations: int, dataset_file: str, tournament_size: int) -> None:
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_swap_probability = mutation_swap_probability
        self.mutation_inversion_probability = mutation_inversion_probability
        self.iterations = iterations
        self.dataset_file = dataset_file
        self.tournament_size = tournament_size
        self.distances = self.load_distances(self.dataset_file)
        self.path_size = len(self.distances)
        self.population = self.generate_population()

        self.best_distance = None
        self.best_path = None


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
    

    def print_distance(self, city_index: int, destination_index: int) -> None:
        print(self.distances[city_index][destination_index])


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
            temp = self.distances[city][path[(i + 1) % path_length]]
            distance += temp
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
                best = path.copy()
                best_distance = self.calculate_distance(path) 
            elif self.calculate_distance(path) < best_distance:
                best = path.copy()
                best_distance = self.calculate_distance(path)
        return best


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
    

    def inversion_mutation(self, probability: float, population: list[list[int]]) -> list[list[int]]:
        for path in population:
            if random.random() < probability:
                x1 = random.randint(0, len(path) - 2)
                x2 = random.randint(x1, len(path) - 1)
                path[x1:x2] = reversed(path[x1:x2])
        return population


    def run_genetic_algorithm(self):
        stagnation_iteration = 0
        try:
            __crossover_probability = self.crossover_probability
            __mutation_swap_probability = self.mutation_swap_probability
            __mutation_inversion_probability = self.mutation_inversion_probability
            previous_best_distance = None
            for iteration in range(self.iterations):
                if stagnation_iteration >= 50:
                    __mutation_swap_probability = random.uniform(0.7, 0.9)
                    __crossover_probability = random.uniform(0.01, 0.2)
                    __mutation_inversion_probability = random.uniform(0.01, 0.2)
                    stagnation_iteration = 0

                self.population = self.tournament_selection(self.population)
                self.population = self.pmx_crossover(__crossover_probability, self.population)
                self.population = self.swap_mutation(__mutation_swap_probability, self.population)
                self.population = self.inversion_mutation(__mutation_inversion_probability, self.population)
                best_path = self.get_best_from_population(self.population)
                best_distance = self.calculate_distance(best_path)

                if best_distance == previous_best_distance:
                    stagnation_iteration += 1
                else:
                    previous_best_distance = best_distance
                    stagnation_iteration = 0

                if iteration == 0:
                    self.best_distance = best_distance
                    self.best_path = best_path
                else:
                    if best_distance < self.best_distance:
                        self.best_distance = best_distance
                        self.best_path = best_path

                print(f"Iteration: {iteration}. Distance: {self.best_distance}   ", end="\r")
        except KeyboardInterrupt:
            print(f"Break at iteration num: {iteration}                  ")
        finally:
            print("------------------------------------------------------")
            print(f"Best path found: {self.best_path}")
            print(f"The distance was: {self.best_distance}")
            # print(len(self.best_path), len(self.best_path) == len(set(self.best_path))) #DEBUG:
            print("------------------------------------------------------")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--population_size", type=int, default=100, help="Size of population") 
    parser.add_argument("--crossover_probability", type=float, default=0.95, help="Probability of crossover")
    parser.add_argument("--mutation_swap_probability", type=float, default=0.05, help="Probability of mutation (swap)") 
    parser.add_argument("--mutation_inversion_probability", type=float, default=0.05, help="Probability of mutation (inversion)") 
    parser.add_argument("--iterations", type=int, default=10000, help="Number of iterations") 
    parser.add_argument("--dataset_file", type=str, default="berlin52.txt", help="Text file with dataset")
    parser.add_argument("--tournament_size", type=int, default=4, help="Size of tournament")  
    args = parser.parse_args()

    genetic_algorithm = GeneticAlgorithm(population_size=args.population_size,
                                         crossover_probability=args.crossover_probability,
                                         mutation_swap_probability=args.mutation_swap_probability,
                                         mutation_inversion_probability=args.mutation_inversion_probability,
                                         iterations=args.iterations,
                                         dataset_file=args.dataset_file,
                                         tournament_size=args.tournament_size)
    genetic_algorithm.run_genetic_algorithm()
