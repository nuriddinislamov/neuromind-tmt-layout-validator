import random

def generate_random_layout(grid_size, node_count):
    """Generate a random layout of nodes within the grid."""
    layout = []
    for _ in range(node_count):
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        layout.append((x, y))
    return layout