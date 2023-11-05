from GeneticAlgorithm import GeneticAlgorithm
import argparse


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
