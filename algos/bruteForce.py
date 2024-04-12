import random
import matplotlib.pyplot as plt

NODE_COUNT = 17
GRID_SIZE = 256

def generate_random_layout():
    layout = []
    for _ in range(NODE_COUNT):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        layout.append((x, y))
    return layout

def paths_cross(layout):
    for i in range(len(layout) - 2):
        for j in range(i + 2, len(layout) - 1):
            if segments_intersect(layout[i], layout[i + 1], layout[j], layout[j + 1]):
                return True
    return False


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
    """Determine orientation of triplet (p, q, r)."""
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def on_segment(p, q, r):
    """Check if point q lies on segment pr."""
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))


def plot_layout(layout):
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

print("Random layout:", layout)
plot_layout(layout)