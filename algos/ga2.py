import random
import matplotlib.pyplot as plt
import json
from datetime import datetime

# Define constants
GRID_SIZE = 256
NODE_COUNT = 15
NODE_RADIUS = 5
POPULATION_SIZE = 100
NUM_GENERATIONS = 1000
MUTATION_RATE = 0.1

def generate_random_layout(grid_size, node_count):
    """
    Generate a random layout of nodes within the grid.
    """
    layout = []
    for _ in range(node_count):
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        layout.append((x, y))
    return layout


def fitness_function(layout, node_radius):
    crossings = count_crossings(layout)
    sparseness_penalty = calculate_sparseness(layout, node_radius)
    penalty = crossings + sparseness_penalty
    return penalty

def count_crossings(layout):
    crossings = 0
    for i in range(len(layout) - 2):
        for j in range(i + 2, len(layout) - 1):
            if segments_intersect(layout[i], layout[i + 1], layout[j], layout[j + 1]):
                crossings += 1
    return crossings

def calculate_sparseness(layout, node_radius):
    total_distance = 0
    for i in range(len(layout) - 1):
        total_distance += distance(layout[i], layout[i + 1])
    average_distance = total_distance / len(layout)
    ideal_distance = 2 * node_radius  # Ideal distance between nodes
    sparseness_penalty = abs(ideal_distance - average_distance)
    return sparseness_penalty

def distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5

def segments_intersect(A, B, C, D):
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special cases
    if o1 == 0 and on_segment(A, C, B):
        return True
    if o2 == 0 and on_segment(A, D, B):
        return True
    if o3 == 0 and on_segment(C, A, D):
        return True
    if o4 == 0 and on_segment(C, B, D):
        return True

    return False

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def on_segment(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def mutate_layout(layout):
    mutated_layout = layout[:]

    index_to_mutate = random.randint(0, len(mutated_layout) - 1)
    
    new_x = random.randint(0, GRID_SIZE - 1)
    new_y = random.randint(0, GRID_SIZE - 1)
    
    mutated_layout[index_to_mutate] = (new_x, new_y)
    
    return mutated_layout

def plot_layout(layout):
    """Plot the layout of nodes."""
    plt.figure(figsize=(5, 5))
    for i, (x, y) in enumerate(layout):
        plt.scatter(x, y, color='yellow', s=200)
        plt.text(x, y, str(i + 1), fontsize=14, ha='center', va='center')
    plt.xlim(-1, GRID_SIZE)
    plt.ylim(-1, GRID_SIZE)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Final Layout')
    plt.grid(True)
    plt.show()

def convert_layout_to_json(layout):
    """Convert the layout to JSON format."""
    json_data = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'node_count': len(layout),
        'layout': layout
    }
    return json.dumps(json_data, indent=4)

# Main loop
population = [generate_random_layout(GRID_SIZE, NODE_COUNT) for _ in range(POPULATION_SIZE)]
best_layout = None
best_fitness = float('inf')
for generation in range(NUM_GENERATIONS):
    for layout in population:
        fitness = fitness_function(layout, NODE_RADIUS)
        if fitness < best_fitness:
            best_layout = layout
            best_fitness = fitness
    population = [mutate_layout(layout) for layout in population]

# Plot the best layout if it exists
if best_layout:
    json_layout = convert_layout_to_json(best_layout)
    print(json_layout)
    plot_layout(best_layout)
else:
    print("No valid layout without edge crossings found.")
