function grid_search(ds)
    fname = strcat('results/hols/', ds, '_grid_search.csv');
    [G, L, label_splits] = load_data(ds, 5);
    deg = full(sum(G{2}, 1));
    % parameters for HOLS
    eta = 0.5;
    eps = 1e-6;
    max_iter = 500;
    verbose = 0;
    % actual grid search
    alphas = dlmread('data/configs.txt');
    num_config = size(alphas, 1);
    accuracies = zeros(num_config, 5);
    dlmwrite(fname, [alphas, accuracies], 'precision', '%.4f');

    for r = 1:5
        vl = label_splits(:, r);
        ll = L(vl);
        fprintf('random run: %d\n', r);
        for i = 1:num_config
            alpha = alphas(i, :);
            [vu, lu, ~] = hols(G, 5, [0 alpha], vl, ll, eta, eps, max_iter, verbose);
            accuracies(i, r) = accuracy(vu, lu, L, deg);
        end
        dlmwrite(fname, [alphas, accuracies]);
    end
end

function acc = accuracy(vu, pred_lu, labels, degree)
    % accuracy comparing to ground truth, on only vertices have degree >= 1
    pred_lu = pred_lu(degree(vu) > 0);
    vu = vu(degree(vu) > 0);
    true_lu = labels(vu);
    acc = sum(true_lu == pred_lu) / numel(vu);
end