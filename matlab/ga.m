function ga
    % Timing
    tic;

    % Define constants
    gridSize = 1024;
    nodeCount = 25;
    populationSize = 100;
    maxGenerations = 1000;
    mutationRate = 0.1;

    population = cell(populationSize, 1);
    for i = 1:populationSize
        population{i} = generateRandomLayout(gridSize, nodeCount);
    end

    hFig = figure;
    hAx = axes('Parent', hFig);

    foundSolution = false;

    for generation = 1:maxGenerations
        % Calculate fitness for each individual
        for i = 1:populationSize
            if is_layout_valid(population{i})
                disp(['Solution found in generation ', num2str(generation)]);
                disp('Layout Coordinates:');
                disp(population{i});
                plotLayout(population{i}, hAx); % Plot final valid layout
                foundSolution = true;
            end
        end

        if foundSolution
            break;
        end

        selectedIndices = selection(population, populationSize);
        
        % Here happens
        % the crossover and mutation process,
        % that is explained more in depth in 
        % the method section of the report
        newPopulation = cell(populationSize, 1);
        for i = 1:2:populationSize-1
            parent1 = population{selectedIndices(i)};
            parent2 = population{selectedIndices(i+1)};
            [child1, child2] = crossover(parent1, parent2);
            newPopulation{i} = mutate(child1, gridSize, mutationRate);
            newPopulation{i+1} = mutate(child2, gridSize, mutationRate);
        end
        population = newPopulation;

        
    end

    if ~foundSolution
        disp('No valid layout found within the maximum number of generations');
    end

    elapsedTime = toc;

    fprintf('Execution Time: %.2f seconds\n', elapsedTime);

    
end

function layout = generateRandomLayout(gridSize, nodeCount)
    layout = rand(nodeCount, 2) * gridSize;
end

function plotLayout(layout, hAx)
    cla(hAx);
    plot(hAx, layout(:, 1), layout(:, 2), 'o-', 'MarkerFaceColor', 'g');
    xlim(hAx, [0, 1024]);
    ylim(hAx, [0, 1024]);
    title('Final Valid Layout');
    drawnow;
end


% This function is used across all
% implementations consistently
% to ensure the validity and integrity
% during testing

% Inspired from is_valid_layout function that is defined in the
% algos/isValidLayout.py file of this project
function is_valid = is_layout_valid(layout)
    num_nodes = size(layout, 1);
    for i = 1:num_nodes-1
        for j = i+2:num_nodes-1
            if segments_intersect(layout(i,:), layout(i+1,:), layout(j,:), layout(j+1,:))
                is_valid = false;
                return;
            end
        end
    end
    is_valid = true;
end

function result = segments_intersect(p1, p2, q1, q2)
    function o = orientation(p, q, r)
        val = (q(2) - p(2)) * (r(1) - q(1)) - (q(1) - p(1)) * (r(2) - q(2));
        if val == 0, o = 0; elseif val > 0, o = 1; else, o = 2; end
    end
    function on_seg = on_segment(p, q, r)
        on_seg = (q(1) <= max(p(1), r(1)) && q(1) >= min(p(1), r(1)) && q(2) <= max(p(2), r(2)) && q(2) >= min(p(2), r(2)));
    end
    o1 = orientation(p1, p2, q1);
    o2 = orientation(p1, p2, q2);
    o3 = orientation(q1, q2, p1);
    o4 = orientation(q1, q2, p2);
    result = (o1 ~= o2 && o3 ~= o4) || (o1 == 0 && on_segment(p1, q1, p2)) || (o2 == 0 && on_segment(p1, q2, p2)) || (o3 == 0 && on_segment(q1, p1, q2)) || (o4 == 0 && on_segment(q1, p2, q2));
end

function indices = selection(population, populationSize)
    fitness = cellfun(@(x) sum(x(:)), population);
    maxFitness = max(fitness);
    adjustedFitness = maxFitness - fitness;
    totalFitness = sum(adjustedFitness);
    probabilities = adjustedFitness / totalFitness;
    cumulativeProbabilities = cumsum(probabilities);
    indices = arrayfun(@(x) find(cumulativeProbabilities >= x, 1, 'first'), rand(populationSize, 1));
end

function [child1, child2] = crossover(parent1, parent2)
    point = randi([1, size(parent1, 1) - 1]);
    child1 = [parent1(1:point, :); parent2(point+1:end, :)];
    child2 = [parent2(1:point, :); parent1(point+1:end, :)];
end

function mutated = mutate(individual, gridSize, mutationRate)
    mutated = individual;
    for i = 1:size(individual, 1)
        if rand() < mutationRate
            mutated(i, :) = rand(1, 2) * gridSize;
        end
    end
end
