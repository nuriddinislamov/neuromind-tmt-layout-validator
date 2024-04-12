import random
import matplotlib.pyplot as plt
import math

GRID_SIZE = 1024
NODE_COUNT = 20
NODE_RADIUS = 5
MARGIN = 10
MIN_DISTANCE_BETWEEN_NODES = 2 * (NODE_RADIUS + MARGIN)
TEMPERATURE_START = 1000
TEMPERATURE_END = 1
COOLING_RATE = 0.95

def create_initial_layout():
    layout = []
    while len(layout) < NODE_COUNT:
        node = (random.randint(NODE_RADIUS, GRID_SIZE - NODE_RADIUS),
                random.randint(NODE_RADIUS, GRID_SIZE - NODE_RADIUS))
        if all(math.hypot(node[0] - other[0], node[1] - other[1]) >= MIN_DISTANCE_BETWEEN_NODES for other in layout):
            layout.append(node)
    return layout

def calculate_energy(layout):
    crossings = count_crossings(layout)
    # Adding sparseness calculation to encourage spread out layouts
    sparseness = calculate_sparseness(layout)
    return crossings + sparseness

def count_crossings(layout):
    crossings = 0
    for i in range(NODE_COUNT):
        for j in range(i + 1, NODE_COUNT):
            if segments_intersect(layout[i], layout[(i + 1) % NODE_COUNT], layout[j], layout[(j + 1) % NODE_COUNT]):
                crossings += 1
    return crossings

def segments_intersect(p1, q1, p2, q2):
    # Function to check if two line segments intersect
    pass  # Implement the segment intersection logic

def calculate_sparseness(layout):
    # Calculate average pairwise distance to encourage spreading out
    distances = [math.hypot(layout[i][0] - layout[j][0], layout[i][1] - layout[j][1])
                 for i in range(NODE_COUNT) for j in range(i + 1, NODE_COUNT)]
    avg_distance = sum(distances) / len(distances)
    # Lower average distance results in higher penalty to discourage clustering
    return -avg_distance

def generate_neighbor(layout):
    # Function to slightly move a node while ensuring it doesn't violate the constraints
    neighbor = layout[:]
    node_index = random.randint(0, NODE_COUNT - 1)
    move_successful = False
    while not move_successful:
        dx = random.randint(-20, 20)  # Adjust these values as necessary
        dy = random.randint(-20, 20)
        new_x = max(NODE_RADIUS, min(GRID_SIZE - NODE_RADIUS, neighbor[node_index][0] + dx))
        new_y = max(NODE_RADIUS, min(GRID_SIZE - NODE_RADIUS, neighbor[node_index][1] + dy))
        new_node = (new_x, new_y)
        if all(math.hypot(new_x - other[0], new_y - other[1]) >= MIN_DISTANCE_BETWEEN_NODES for i, other in enumerate(neighbor) if i != node_index):
            neighbor[node_index] = new_node
            move_successful = True
    return neighbor

def simulated_annealing():
    current_layout = create_initial_layout()
    current_energy = calculate_energy(current_layout)
    temperature = TEMPERATURE_START
    
    while temperature > TEMPERATURE_END:
        neighbor = generate_neighbor(current_layout)
        neighbor_energy = calculate_energy(neighbor)
        energy_change = neighbor_energy - current_energy
        
        if energy_change < 0 or random.random() < math.exp(-energy_change / temperature):
            current_layout = neighbor
            current_energy = neighbor_energy
        
        temperature *= COOLING_RATE
    
    return current_layout

def plot_layout(layout):
    fig, ax = plt.subplots(figsize=(10, 10))

    for node in layout:
        circle_area = math.pi * (NODE_RADIUS ** 2) * 10  # Adjust the multiplier as needed for visibility
        circle = plt.Circle(node, circle_area, color='yellow', alpha=0.5, edgecolor='black')
        ax.add_artist(circle)
    ax.set_xlim(0, GRID_SIZE)
    ax.set_ylim(0, GRID_SIZE)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.show()

final_layout = simulated_annealing()
plot_layout(final_layout)