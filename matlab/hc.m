function hc
    layout_size = 1024;
    num_nodes = 5;
    layout = rand(num_nodes, 2) * layout_size;
    max_iterations = 1000;
    iteration = 0;    
    min_intersections = Inf;
    best_layout = layout;
    
    while iteration < max_iterations
        new_layout = best_layout;
        idx = randperm(num_nodes, 2);
        temp = new_layout(idx(1), :);
        new_layout(idx(1), :) = new_layout(idx(2), :);
        new_layout(idx(2), :) = temp;
        
        if is_layout_valid(new_layout)
            current_intersections = count_intersections(new_layout);
            if current_intersections < min_intersections
                min_intersections = current_intersections;
                best_layout = new_layout;
            end
        end
        
        iteration = iteration + 1;
    end
    
    plot_layout(best_layout);
    
end

function isValid = is_layout_valid(layout)
    numNodes = size(layout, 1);
    isValid = true;
    
    for i = 1:numNodes-1
        for j = i+1:numNodes
            if i ~= j && segments_intersect(layout(i, :), layout(i+1, :), layout(j, :), layout(j+1, :))
                isValid = false;
                return;
            end
        end
    end
end

function result = segments_intersect(p1, p2, q1, q2)
    result = false;
    
    o1 = orientation(p1, p2, q1);
    o2 = orientation(p1, p2, q2);
    o3 = orientation(q1, q2, p1);
    o4 = orientation(q1, q2, p2);
    
    if o1 ~= o2 && o3 ~= o4
        result = true;
    elseif o1 == 0 && on_segment(p1, q1, p2)
        result = true;
    elseif o2 == 0 && on_segment(p1, q2, p2)
        result = true;
    elseif o3 == 0 && on_segment(q1, p1, q2)
        result = true;
    elseif o4 == 0 && on_segment(q1, p2, q2)
        result = true;
    end
end

function o = orientation(p, q, r)
    val = (q(2) - p(2)) * (r(1) - q(1)) - (q(1) - p(1)) * (r(2) - q(2));
    if val == 0
        o = 0; % collinear
    elseif val > 0
        o = 1; % clockwise
    else
        o = 2; % counter-clockwise
    end
end

function isOn = on_segment(p, q, r)
    isOn = (min(p(1), r(1)) <= q(1) && q(1) <= max(p(1), r(1))) && ...
           (min(p(2), r(2)) <= q(2) && q(2) <= max(p(2), r(2)));
end

function plot_layout(layout)
    x = layout(:, 1);
    y = layout(:, 2);
    
    figure;
    plot(x, y, 'o', 'MarkerSize', 10, 'MarkerFaceColor', 'b');
    hold on;
    
    for i = 1:length(x)
        text(x(i), y(i), sprintf('%d', i), ...
            'HorizontalAlignment', 'center', ...
            'VerticalAlignment', 'middle', ...
            'Color', 'White');
    end
    
    axis([0 1024 0 1024]);
    axis square;
    
    xlabel('X-coordinate');
    ylabel('Y-coordinate');
    title('Layout of Nodes with Numbering');
    
    grid on;
    hold off;
end
