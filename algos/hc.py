import matplotlib.pyplot as plt
import matplotlib.patches as patches

coordinates = [
    (518, 331),
    (429, 389),
    (410, 390),
    (595, 464),
    (608, 164),
    (379, 194),
    (506, 247),
    (342, 313),
    (254, 393),
    (266, 486),
    (361, 451),
    (430, 557),
    (80, 542),
    (197, 304),
    (55, 342),
    (57, 18),
    (64, 66),
    (172, 126),
    (242, 58),
    (262, 192),
    (445, 104),
    (360, 49),
    (371, 43),
    (578, 47),
    (720, 108)
    # [767, 531],
    # [675, 348],
    # [635, 521]
]

# Plotting function
def plot_layout(coordinates):
    # Create a scatter plot for the nodes
    fig, ax = plt.subplots()
    ax.scatter(*zip(*coordinates), s=100, c='white', edgecolors='black', linewidth=1)  # Node size is arbitrarily set to 1000 for visibility

    # Annotate each node with its number
    # for i, (x, y) in enumerate(coordinates, start=1):
        # ax.text(x, y, str(i), color='black', fontsize=12, ha='center', va='center')

    # Set the aspect of the plot to be equal and remove axes
    # ax.set_aspect('equal')
    # ax.axis('off')

    # Set the size of the plot to match the aspect ratio of the layout
    ax.set_xlim(0, 1024)
    ax.set_ylim(0, 1024)

    # Show the plot
    # plt.gca().invert_yaxis()  # Invert y-axis to match the coordinate input with the visual output
    plt.show()

# Run the plotting function with the given coordinates
plot_layout(coordinates)
