import random
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

def create_individual():
    return [(random.uniform(NODE_RADIUS, GRID_WIDTH - NODE_RADIUS),
             random.uniform(NODE_RADIUS, GRID_HEIGHT - NODE_RADIUS)) for _ in range(NUM_NODES)]

def calculate_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def eval_placement(individual):
    total_distance = 0
    min_distance = float('inf')  # Initialize with infinity

    # Calculate the minimum distance between nodes to maximize sparsity
    for i in range(NUM_NODES):
        for j in range(i + 1, NUM_NODES):
            dist = calculate_distance(individual[i], individual[j])
            min_distance = min(min_distance, dist)

    # Calculate total distance for the path (this could be part of another objective)
    for i in range(NUM_NODES - 1):
        total_distance += calculate_distance(individual[i], individual[i + 1])

    # Compute a sparsity score, larger is better, so we take negative to minimize in GA
    sparsity_score = -min_distance

    # Return a tuple including the sparsity score
    return total_distance, sparsity_score,

def mutate_individual(individual):
    """Mutate an individual by randomly adjusting the position of a node."""
    for i in range(len(individual)):
        if random.random() < MUTPB:
            individual[i] = (random.uniform(NODE_RADIUS, GRID_WIDTH - NODE_RADIUS),
                             random.uniform(NODE_RADIUS, GRID_HEIGHT - NODE_RADIUS))
    return individual,

def orientation(p, q, r):
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if val == 0: return 0  # colinear
    return 1 if val > 0 else 2  # clock or counterclock wise

def on_segment(p, q, r):
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
        return True
    return False

def intersect(seg1_start, seg1_end, seg2_start, seg2_end):
    """
    Return True if line segments (p1, q1) and (p2, q2) intersect, otherwise False.
    """
    # Find the four orientations needed for general and special cases
    o1 = orientation(seg1_start, seg1_end, seg2_start)
    o2 = orientation(seg1_start, seg1_end, seg2_end)
    o3 = orientation(seg2_start, seg2_end, seg1_start)
    o4 = orientation(seg2_start, seg2_end, seg1_end)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special Cases
    if o1 == 0 and on_segment(seg1_start, seg2_start, seg1_end): return True
    if o2 == 0 and on_segment(seg1_start, seg2_end, seg1_end): return True
    if o3 == 0 and on_segment(seg2_start, seg1_start, seg2_end): return True
    if o4 == 0 and on_segment(seg2_start, seg1_end, seg2_end): return True

    return False  # Doesn't fall in any of the above cases

# Fitness and Individual
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))  # Note the weights
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutate_individual)
toolbox.register("select", tools.selNSGA2)  # Using NSGA-II for multi-objective optimization
toolbox.register("evaluate", eval_placement)
toolbox.register("mate", tools.cxTwoPoint)

# Constants
NUM_NODES = 20
GRID_WIDTH = 1024
GRID_HEIGHT = 1024
NODE_DIAMETER = 10
NODE_RADIUS = NODE_DIAMETER / 2
POPULATION_SIZE = 1000
NUM_GENERATIONS = 250
CXPB, MUTPB = 0.8, 0.2


def main():
    pop = toolbox.population(n=POPULATION_SIZE)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", min)

    # Main GA loop with dynamic random seeds
    final_pop, logbook = algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, NUM_GENERATIONS,
                                             stats=stats, halloffame=hof, verbose=True)

    return final_pop, logbook, hof

if __name__ == "__main__":
    final_pop, logbook, hof = main()

    # Visualize the best individual
    best_ind = hof.items[0]
    plt.figure(figsize=(GRID_WIDTH / 100, GRID_HEIGHT / 100))
    for i, node in enumerate(best_ind):
        plt.plot(node[0], node[1], 'o', markersize=NODE_DIAMETER, label=str(i+1) if i == 0 else "")
        plt.text(node[0], node[1], str(i+1), ha='center', va='center')
    for i in range(NUM_NODES - 1):
        plt.plot((best_ind[i][0], best_ind[i+1][0]), (best_ind[i][1], best_ind[i+1][1]), 'k-')

    plt.xlim(0, GRID_WIDTH)
    plt.ylim(0, GRID_HEIGHT)
    plt.title("Optimized Node Layout")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.show()
