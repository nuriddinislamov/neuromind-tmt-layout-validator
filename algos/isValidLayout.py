def is_layout_valid(layout):
    def segments_intersect(p1, p2, q1, q2):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # collinear
            elif val > 0:
                return 1  # clockwise
            else:
                return 2  # counter-clockwise
        
        def on_segment(p, q, r):
            if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
                return True
            return False
        
        o1 = orientation(p1, p2, q1)
        o2 = orientation(p1, p2, q2)
        o3 = orientation(q1, q2, p1)
        o4 = orientation(q1, q2, p2)
        
        # General case
        if o1 != o2 and o3 != o4:
            return True
        
        # Special cases - Checking if the points are collinear and on segment
        if o1 == 0 and on_segment(p1, q1, p2): return True
        if o2 == 0 and on_segment(p1, q2, p2): return True
        if o3 == 0 and on_segment(q1, p1, q2): return True
        if o4 == 0 and on_segment(q1, p2, q2): return True
        
        return False
    
    num_nodes = len(layout)
    for i in range(num_nodes - 1):
        for j in range(i + 2, num_nodes - 1):
            if segments_intersect(layout[i], layout[i + 1], layout[j], layout[j + 1]):
                return False
    
    return True

# layout = [[2, 2], [2, 4], [4, 3], [3, 3]]
layout = \
    [(992, 749), (757, 621), (613, 504), (666, 893), (285, 834), (229, 892), (533, 920), (794, 873), (670, 635), (755, 845), (174, 746), (324, 333), (386, 280), (499, 117), (530, 118), (490, 451), (425, 612), (144, 713), (451, 477), (876, 142)]
validity = is_layout_valid(layout)
print(f"Is the layout valid? {'Yes' if validity else 'No'}")
