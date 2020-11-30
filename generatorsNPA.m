function generators = generatorsNPA(n, m, l)
% Computes the symmetry generators for an NPA matrix
%
% Here, we focus on the case of homogeneous Bell scenario, in which n
% parties all have the same number of measurement settings m, with same
% number of possible outcomes k. Moreover, we fix k=2.
%
% The parametrization used here is in terms of correlators. Therefore, the
% permutations are signed permutations.
%
% Args:
%   n (integer >= 1) : number of parties
%   m (integer >= 1) : number of measurement settings
%   l (integer >= 1) : local level of the hierarchy
%
% Returns:
%   cell array of signed permutations : the list of generators
%
% Example:
%   >> generators = generatorsNPA(2, 2, 2)
%   >> group = replab.SignedPermutationGroup(length(generators{1}), generators)
%   >> rep = group.naturalRep
%   >> dec = rep.decomposition

% Written by Jean-Daniel Bancal on 26 Nov. 2020

% The initial set of operators
operators0 = [0:m].';

% We increase the level of operators
operators = operators0;
for i = 1:l-1
    op1 = kron(operators, ones(1+m,1));
    op2 = kron(ones(size(operators,1),1), operators0);
    operators = [op1, op2];
end

% We simplify all products of operators
for i = 1:size(operators,1)
    lastOp = 0;
    lastj = 0;
    for j = 1:size(operators,2)
        if operators(i,j) ~= 0
            if lastOp ~= operators(i,j)
                lastOp = operators(i,j);
                lastj = j;
            else
                % A*A=Id
                operators(i, [lastj j]) = 0;
            end
        end
    end
end

% put the zeros at the end
for i = 1:size(operators,1)
    line = operators(i,:);
    nonZ = (line ~= 0);
    operators(i,:) = 0;
    operators(i,1:sum(nonZ)) = line(nonZ);
end

% remove duplicates
operators = unique(operators, 'rows');
nbOpA = size(operators,1);

% compute the image of group generators for measurement relabelling on one
% party
switch m
    case 1
        gensS = {};
    case 2
        gensS = {[2 1]};
    otherwise
        gensS = {[2 1 3:m] [2:m 1]};
end
genA = {};
for i = 1:length(gensS)
    imageOperators = 0*operators;
    for j = 1:m
        imageOperators(operators == j) = gensS{i}(j);
    end
    [C, IA, IC] = unique(imageOperators,'rows');
    assert(isequal(operators,C));
    genA{end+1} = IC.';
end

% lift these permutations to the multipartite case
genAFull = cell(size(genA));
for i = 1:length(genA)
    genAFull{i} = kron(ones(1,nbOpA^(n-1)), genA{i}) + kron(nbOpA*[0:nbOpA^(n-1)-1], ones(1,nbOpA));
    assert(length(unique(genAFull{i})) == nbOpA^n);
end

% compute the sign effect of permuting the first outcome of Alice
signsA1 = (-1).^sum(operators==1,2).';
genA1 = signsA1.*[1:nbOpA];

% lift this permutation to the multipartite case
genA1Full = kron(ones(1,nbOpA^(n-1)), signsA1).*[1:nbOpA^n];

% compute the effect of permuting the parties
switch n
    case 1
        gensP = {};
    case 2
        gensP = {[2 1]};
    otherwise
        gensP = {[2 1 3:n] [2:n 1]};
end
genAB = {};
M = reshape(1:nbOpA^n, nbOpA*ones(1,n));
for i = 1:length(gensP)
    imM = permute(M, gensP{i});
    genAB{end+1} = imM(:).';
end

% Finally, we gather all signed generators in a single list
generators = [genAB, genAFull, genA1Full];




