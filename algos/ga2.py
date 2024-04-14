import random
import matplotlib.pyplot as plt

def plot_layout(layout):
    x, y = zip(*layout)
    plt.figure(figsize=(10, 10))
    plt.scatter(x, y, c='blue', marker='o')
    for i in range(len(layout)):
        plt.text(layout[i][0], layout[i][1], str(i+1), color="red", fontsize=12, ha='center')
    plt.title('Trail Making Test Layout')
    plt.grid(True)
    plt.xlim(0, 1000)
    plt.ylim(0, 1000)
    plt.show()

def is_layout_valid(layout):
    def segments_intersect(p1, p2, q1, q2):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  
            elif val > 0:
                return 1  
            else:
                return 2 

        def on_segment(p, q, r):
            if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
                return True
            return False

        o1 = orientation(p1, p2, q1)
        o2 = orientation(p1, p2, q2)
        o3 = orientation(q1, q2, p1)
        o4 = orientation(q1, q2, p2)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and on_segment(p1, q1, p2): return True
        if o2 == 0 and on_segment(p1, q2, p2): return True
        if o3 == 0 and on_segment(q1, p1, q2): return True
        if o4 == 0 and on_segment(q1, p2, q2): return True

        return False

    num_nodes = len(layout)
    valid_segments = 0
    for i in range(num_nodes - 1):
        for j in range(i + 1, num_nodes):
            if not segments_intersect(layout[i], layout[(i + 1) % num_nodes], layout[j], layout[(j + 1) % num_nodes]):
                valid_segments += 1
    return valid_segments

def initialize_population(size, num_nodes, grid_size):
    return [[(random.randint(0, grid_size), random.randint(0, grid_size)) for _ in range(num_nodes)] for _ in range(size)]

def compute_fitness(population):
    return [is_layout_valid(layout) for layout in population]

def select_parents(population, fitness, num_parents):
    return random.choices(population, weights=fitness, k=num_parents)

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]

def mutate(layout, mutation_rate, grid_size):
    for i in range(len(layout)):
        if random.random() < mutation_rate:
            layout[i] = (random.randint(0, grid_size), random.randint(0, grid_size))
    return layout

def genetic_algorithm(grid_size=1024, num_nodes=25, population_size=50, generations=100, mutation_rate=0.01):
    population = initialize_population(population_size, num_nodes, grid_size)
    grid = grid_size
    h = {"grid_size": grid}
    for _ in range(generations):
        fitness = compute_fitness(population)
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, fitness, 2)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate, grid_size)
            new_population.append(child)
        population = new_population
    fitness = compute_fitness(population)
    best_index = fitness.index(max(fitness))
    best_layout = population[best_index]
    h["layout"] = best_layout

    # Uncommenting the following line (97) will break the API
    # as it is designed to plot the coordinates on a visual graph
    # for debugging and development purposes only


    # plot_layout(best_layout)
    return h
