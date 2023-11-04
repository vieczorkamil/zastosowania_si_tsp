from GeneticAlgorithm import GeneticAlgorithm



POPULATION_SIZE         = 11
CROSSOVER_PROBABILITY   = 0.9
MUTATION_PROBABILITY    = 0.1
ITERATIONS              = 100000
DATASET_FILE            = "berlin52.txt"
TOURNAMENT_SIZE         = 70


if __name__ == "__main__":
    genetic_algorithm = GeneticAlgorithm(POPULATION_SIZE, CROSSOVER_PROBABILITY, MUTATION_PROBABILITY, ITERATIONS, DATASET_FILE, TOURNAMENT_SIZE)
    genetic_algorithm.run_genetic_algorithm()
