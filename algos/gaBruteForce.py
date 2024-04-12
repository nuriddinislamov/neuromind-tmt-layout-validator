import random
import matplotlib.pyplot as plt

# Define grid dimensions
GRID_SIZE = 10
NODE_DIAMETER = 10
NODE_COUNT = 18

# Define parameters for the fitness function
CROSSING_PENALTY = 1000  # Penalty for crossing edges
SPARSENESS_PENALTY = 1  # Penalty for sparse layouts

def generate_random_layout():
    """Generate a random layout of nodes within the grid."""
    layout = []
    for _ in range(NODE_COUNT):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        layout.append((x, y))
    return layout

def fitness_function(layout):
    """Evaluate the fitness of a layout."""
    penalty = 0
    # Check for edge crossings
    for i in range(len(layout) - 1):
        for j in range(i + 2, len(layout) - 1):
            if paths_cross(layout):
                penalty += CROSSING_PENALTY

    # Calculate sparseness penalty
    sparseness_penalty = calculate_sparseness(layout)
    penalty += sparseness_penalty
    return penalty


def paths_cross(layout):
    """Check if any edges in the layout intersect."""
    for i in range(len(layout) - 2):
        for j in range(i + 2, len(layout) - 1):
            if segments_intersect(layout[i], layout[i + 1], layout[j], layout[j + 1]):
                return True
    return False

def segments_intersect(A, B, C, D):
    """Check if line segments AB and CD intersect."""
    # Determine orientations
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
    """Determine orientation of triplet (p, q, r)."""
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Colinear
    return 1 if val > 0 else 2  # Clockwise or counterclockwise

def on_segment(p, q, r):
    """Check if point q lies on segment pr."""
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def calculate_sparseness(layout):
    """Calculate the sparseness penalty of a layout."""
    # Calculate the average distance between nodes
    total_distance = sum(abs(layout[i][0] - layout[i + 1][0]) + abs(layout[i][1] - layout[i + 1][1]) for i in range(len(layout) - 1))
    average_distance = total_distance / len(layout)
    # Calculate the penalty based on the average distance
    sparseness_penalty = (GRID_SIZE * NODE_COUNT) - average_distance
    return max(0, sparseness_penalty) * SPARSENESS_PENALTY

def plot_layout(layout):
    """Plot the layout of nodes."""
    plt.figure(figsize=(6, 6))
    for i, (x, y) in enumerate(layout):
        plt.scatter(x, y, color='yellow')
        plt.text(x, y, str(i + 1), fontsize=10, ha='center', va='center')
    plt.xlim(-1, GRID_SIZE)
    plt.ylim(-1, GRID_SIZE)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Random Layout')
    plt.grid(True)
    plt.show()

# Main
valid_layout = False
while not valid_layout:
    layout = generate_random_layout()
    print(layout)
    if not paths_cross(layout):
        valid_layout = True

fitness = fitness_function(layout)
print("Random layout:", layout)
print("Fitness:", fitness)
plot_layout(layout)
