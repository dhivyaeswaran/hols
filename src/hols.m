function [vu, lu, Yu] = hols(G, n, alpha, vl, ll, eta, eps, max_iter, verbose)
    % Returns list of unlabeled vertices and their labels after label
    % spreading. Ties are broken randomly.
    if verbose == 1
        overallTime = tic;
    end
    lap = get_laplacian(G, n, alpha);
    N = size(lap, 1);
    C = max(ll);
    % unlabeled vertices
    vu = setdiff(1:N, vl);
    % prior
    Y0 = ones(N, C) / C;
    for i = 1:numel(ll)
        Y0(vl(i), :) = 0;
        Y0(vl(i), ll(i)) = 1; 
    end
    % label spreading
    curr_eps = 1000;
    num_iter = 0;
    iterTime = tic;
    Y = Y0;
    while (curr_eps > eps) && (num_iter < max_iter)
        num_iter = num_iter + 1;
        Yold = Y;
        Y = eta * (speye(N) - lap) * Y + (1 - eta) * Y0;
        curr_eps = max(abs(Yold - Y), [], 'all');
        if verbose == 1
            if mod(num_iter, 50) == 0
                if num_iter == 50
                    fprintf('[%1.4fs/it] ', toc(iterTime) / 50);
                end
                fprintf('%d (%1.1f) ', num_iter, curr_eps / eps);
            end
        end
    end
    if verbose == 1
            fprintf('[%d it, eps %1.1f, %1.4fs]\n', num_iter, curr_eps / eps, toc(overallTime));
    end
    % find best label
    Yu = Y(vu, :);
    lu = probabilities_to_labels(Yu);
end

function lu = probabilities_to_labels(Yu)
    rng(0);
%     [~, lu] = max(Yu, [], 2);
%     lu = transpose(lu);
    nu = size(Yu, 1);
    lu = zeros(1, nu);
    for i = 1:nu
        ind = find(Yu(i, :) == max(Yu(i, :)));
        ind = ind(randperm(numel(ind)));
        lu(i) = ind(1);
    end
end

function lap = get_laplacian(G, n, alpha)
    assert(numel(alpha) == n);
    eps = 0.00001;
    assert(1 - eps < sum(alpha) < 1 + eps);
    assert(alpha(1) == 0);

    adj = alpha(2) * G{2};
    for k=3:n
        adj = adj + alpha(k) * G{k};
    end
    lap = speye(size(G{2}, 1)) - sym_norm(adj);
end

function m = sym_norm(m)
    d = max(sum(m,1), 1e-12);
    m = diag(d.^(-0.5)) * m * diag(d.^(-0.5));
end
