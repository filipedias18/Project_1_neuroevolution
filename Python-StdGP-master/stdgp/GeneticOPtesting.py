from GeneticOperators import *
import random

# Define the population as a list of individuals (assuming their fitness score is sorted in decreasing order)
population = ['Individual1', 'Individual2', 'Individual3', 'Individual4', 'Individual5']

# Set the tournament size
candidates_in_tournament = 2

# Create a random number generator
rng = random.Random(123)

# Select individuals for the tournament
tournament_candidates = [population[i] for i in [rng.randint(0, len(population)-1) for j in range(candidates_in_tournament)]]

# Use the tournament function to select an individual
selected_individual = tournament(rng, population, candidates_in_tournament)

# Print the selected individual and the individuals selected for the tournament
print("Selected Individual:", selected_individual)
print("Tournament Candidates:", tournament_candidates)


def double_tournament(tournament_size, parsimony_tournament_size, population, n, fitness_first=True):
    if fitness_first:
        if tournament_size >= parsimony_tournament_size:
            tournament_order = ['fitness', 'size']
        else:
            print("The parsimony size must be smaller or equal than the tournament size.")
    else:
        if tournament_size <= parsimony_tournament_size:
            tournament_order = ['size', 'fitness']
        else:
            print("The tournament size must be smaller or equal than the parsimony size.")

    # Run the tournaments in order
    for current_tournament in tournament_order:
        # Select contestants for the current tournament
        if current_tournament == 'fitness':
            contestants = [tournament(random, population, n) for i in range(
                tournament_size)]  # n is the number of individuals from the population that will go to the tournament
            # print(contestants)
        else:
            contestants = [size_tournament(random, population, n)for i in range(
                tournament_size)]
            # Run the tournament and get the winner
        if current_tournament == 'fitness':
            winner = [tournament(random, contestants, n) for i in range(parsimony_tournament_size)]
        else:
            winner = [size_tournament(random, contestants, n) for i in range(parsimony_tournament_size)]

    # Return the winner of the final tournament
    return winner

double_tournament(10, 2, population, 3)