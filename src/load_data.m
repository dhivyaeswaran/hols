function [G, L, label_splits] = load_data(ds, k_max)
    % Loads k-clique participation matrices for k = 2, .., k_max,
    % labels for all vertices, and splits for labeled vertcies.
    % Both vertices and labels are indexed from 1.
    file_path = strcat('data/', ds, '/');
    G = cell(k_max, 1);
    for k = 2:k_max
        data = readmatrix(strcat(file_path, int2str(k), 'clique_matrix.txt'));
        data(:, 1:2) = data(:, 1:2) + 1;
        if k == 2
            G{k} = spconvert(data);
        else
            n = size(G{2}, 1);
            G{k} = spconvert([data; n, n, 0]);
        end
    end
    L = transpose(readmatrix(strcat(file_path, 'labels.txt')) + 1);
    label_splits = [];
    for r=1:5
        label_splits = [label_splits, dlmread(strcat(file_path, 'labels', int2str(r), '.txt'))];
    end
    label_splits = label_splits + 1;
end