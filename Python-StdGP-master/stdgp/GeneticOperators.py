from .Individual import Individual
from .Node import Node


#
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-StdGP
#
# Copyright ©2019-2022 J. E. Batista
#
def double_tournament(rng, population, tournament_size, parsimony_tournament_size, number_of_tournaments,
                      fitness_first):
    if fitness_first:
        if tournament_size >= parsimony_tournament_size:
            tournament_order = ['fitness', 'size']
        else:
            print("The parsimony size must be smaller or equal than the number of tournaments.")

    else:
        if tournament_size <= parsimony_tournament_size:
            tournament_order = ['size', 'fitness']
        else:
            print("The number of tournament must be smaller or equal than the parsimony size.")


    # See which type of tournament will be performed first
    if tournament_order[0] == 'fitness':
        contestants = [tournament(rng, population, tournament_size) for i in range(number_of_tournaments)]
    else:
        contestants = [size_tournament(rng, population, tournament_size) for i in range(number_of_tournaments)]

    if tournament_order[1] == 'fitness':
        winner = tournament(rng, contestants, parsimony_tournament_size)
    else:
        winner = size_tournament(rng, contestants, parsimony_tournament_size)

    # Return the winner of the final tournament
    return winner


def size_tournament(rng, population, n):
    '''
    Selects "n" Individuals from the population based on their size
    and returns a single Individual.

    Parameters:
    population (list): A list of Individuals.
    '''
    candidates = [rng.randint(0, len(population) - 1) for i in range(n)]
    return min([population[candidate] for candidate in candidates], key=lambda x: x.getSize())


def tournament(rng, population, n):
    '''
	Selects "n" Individuals from the population and return a 
	single Individual.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
    candidates = [rng.randint(0, len(population) - 1) for i in range(n)]
    return population[min(candidates)]


def getElite(population, n):
    '''
	Returns the "n" best Individuals in the population.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
    return population[:n]


def getOffspring(rng, population, tournament_size, parsimony_tournament_size, number_of_tournaments, fitness_first=True):
    '''
	Genetic Operator: Selects a genetic operator and returns a list with the 
	offspring Individuals. The crossover GOs return two Individuals and the
	mutation GO returns one individual. Individuals over the LIMIT_DEPTH are 
	then excluded, making it possible for this method to return an empty list.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
    isCross = rng.random() < 0.5

    desc = None

    if isCross:
        desc = STXO(rng, population, tournament_size, parsimony_tournament_size, number_of_tournaments, fitness_first=True)
    else:
        desc = STMUT(rng, population, tournament_size, parsimony_tournament_size, number_of_tournaments, fitness_first=True)

    return desc


def discardDeep(population, limit):
    ret = []
    for ind in population:
        if ind.getDepth() <= limit:
            ret.append(ind)
    return ret


def STXO(rng, population, tournament_size, parsimony_tournament_size, number_of_tournaments, fitness_first=True):
    '''
	Randomly selects one node from each of two individuals; swaps the node and
	sub-nodes; and returns the two new Individuals as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
    ind1 = double_tournament(rng, population, tournament_size, parsimony_tournament_size, number_of_tournaments,
                             fitness_first)  # double_tournament(rng,tournament_size, parsimony_tournament_size, population, n, fitness_first)
    ind2 = double_tournament(rng, population, tournament_size, parsimony_tournament_size, number_of_tournaments,
                             fitness_first)

    h1 = ind1.getHead()
    h2 = ind2.getHead()

    n1 = h1.getRandomNode(rng)
    n2 = h2.getRandomNode(rng)

    n1.swap(n2)

    ret = []
    for h in [h1, h2]:
        i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
        i.copy(h)
        ret.append(i)
    return ret


def STMUT(rng, population, tournament_size, parsimony_tournament_size, number_of_tournaments, fitness_first=True):
    '''
	Randomly selects one node from a single individual; swaps the node with a 
	new, node generated using Grow; and returns the new Individual as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
    ind1 = double_tournament(rng, population, tournament_size, parsimony_tournament_size, number_of_tournaments,
                             fitness_first)
    h1 = ind1.getHead()
    n1 = h1.getRandomNode(rng)
    n = Node()
    n.create(rng, ind1.operators, ind1.terminals, ind1.max_depth)
    n1.swap(n)

    ret = []
    i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
    i.copy(h1)
    ret.append(i)
    return ret
