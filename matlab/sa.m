function sa
    numNodes = 10;
    gridSize = 1024;
    T_initial = 1000;   % Initial temperature
    T_final = 1;        % Final temperature
    alpha = 0.95;       % Cooling rate
    maxIterations = 1000; % can be adjusted
    
    layout = [rand(numNodes, 1) * gridSize, rand(numNodes, 1) * gridSize];

    T = T_initial;
    while T > T_final
        for iter = 1:maxIterations
            newLayout = layout;
            nodeIndex = randi(numNodes);
            perturbation = (rand(2, 1) - 0.5) * gridSize * 0.05;
            newLayout(nodeIndex, :) = newLayout(nodeIndex, :) + perturbation';
            
            newLayout(nodeIndex, :) = min(max(newLayout(nodeIndex, :), 0), gridSize);
            
            if is_layout_valid(newLayout, numNodes)
                layout = newLayout;
            end
        end
        T = T * alpha; % cooldown
    end
    
    % plotting
    figure;
    hold on;
    axis([0 gridSize 0 gridSize]);
    scatter(layout(:,1), layout(:,2), 'filled', 'SizeData', 100);
    for i = 1:numNodes
        text(layout(i,1), layout(i,2), num2str(i), ...
            'HorizontalAlignment', 'center', ...
            'VerticalAlignment', 'middle', ...
            'Color', 'white');
    end
    hold off;
end

function valid = is_layout_valid(layout, numNodes)
    valid = true;
    for i = 1:numNodes-1
        for j = i+1:numNodes
            for k = 1:numNodes-1
                for l = k+1:numNodes
                    if (i ~= k && i ~= l && j ~= k && j ~= l)
                        if segments_intersect(layout(i,:), layout(j,:), layout(k,:), layout(l,:))
                            valid = false;
                            return;
                        end
                    end
                end
            end
        end
    end
end

function intersect = segments_intersect(p1, p2, q1, q2)
    if is_collinear(p1, q1, p2) && on_segment(p1, q1, p2) ...
            || is_collinear(p1, q2, p2) && on_segment(p1, q2, p2) ...
            || is_collinear(q1, p1, q2) && on_segment(q1, p1, q2) ...
            || is_collinear(q1, p2, q2) && on_segment(q1, p2, q2)
        intersect = true;
    else
        o1 = orientation(p1, p2, q1);
        o2 = orientation(p1, p2, q2);
        o3 = orientation(q1, q2, p1);
        o4 = orientation(q1, q2, p2);
        intersect = (o1 ~= o2 && o3 ~= o4);
    end
end

function col = is_collinear(p, q, r)
    col = (q(2) - p(2)) * (r(1) - q(1)) == (q(1) - p(1)) * (r(2) - q(2));
end

function onSeg = on_segment(p, q, r)
    onSeg = q(1) <= max(p(1), r(1)) && q(1) >= min(p(1), r(1)) ...
        && q(2) <= max(p(2), r(2)) && q(2) >= min(p(2), r(2));
end

function o = orientation(p, q, r)
    val = (q(2) - p(2)) * (r(1) - q(1)) - (q(1) - p(1)) * (r(2) - q(2));
    if val == 0
        o = 0; 
    elseif val > 0
        o = 1;
    else
        o = 2;
    end
end