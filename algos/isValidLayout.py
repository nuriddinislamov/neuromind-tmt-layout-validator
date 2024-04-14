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