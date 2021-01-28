% initiate RepLAB in its folder (folder address must be edited in)
cd ../replab-0.9.0;
replab_init
cd ../RepCert

%%%%%%%%%%%%%%%%%%%%%%%%%
% FINITE GROUP EXAMPLES %
%%%%%%%%%%%%%%%%%%%%%%%%%

%
%% Example 1: permutation group, tensor power representation
% 
% disp("Permutation group example.")
% disp(" ")
% disp("Group = S8, rep: 4-th tensor power of the natural representation.")
% disp(" ")
% 
% Sn  = replab.S(8)
% nat = Sn.naturalRep;
% rep = kron(nat,kron(nat,nat)) %4th tensor power of natural rep.
% rep = rep.complexification;
% rep = rep.unitarize;
% 
% % decompose
% decomp = rep.decomposition
% 
% % select some random irrep
% randcomp  = decomp.component(randi(decomp.nComponents));
% randirrep = randcomp.irrep(randi(randcomp.nIrreps));
% basis = randirrep.basis;
% 
% %
% % using p_thr. = 10^-7, notice that basis is a gobal_dim x irrep_dim matrix
% numb_group_samples = ceil(7*8*log(10)+2*log(size(basis)(2)))
% subspace_dimension = size(basis)(2)
% 
% % sample random generators
% i = 1; gens = {};
% while i < numb_group_samples
%   g = Sn.sample;
%   gens{i}=g;
%   if g!=Sn.inverse(g)
%     gens{i+1}=Sn.inverse(g);
%     numb_group_samples+=1;
%     i+=1;
%   endif
%   i+=1;
% endwhile
% 
% l = size(gens)(2); % gens is a 1 x |gens| matrix
% i = 1;
% gen_ims = {};
% while i < l+1
%   gen_ims{i} = rep.image(gens{i});
%   i+=1;
% endwhile
% 
% 
% 
% % % save files: (v7 is used so scipy can read them being octave outputs)
% cd InFiles
% save -v7 basis.mat basis
% save -v7 gen_ims.mat gen_ims
% cd ..

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%
%% Example 2: somewhat random tensor product of permutation group irreps
%
%% Note: it seems replab is not producing a good-quality decomposition here.
% 
% disp("Product of two random S4 irreps.")
% disp(" ")
% 
% % group
% Sn = replab.S(4)
% nat = Sn.naturalRep;
% 
% % big rep
% bigrep = kron(nat,nat);
% bigrep = bigrep.complexification;
% bigrep = bigrep.unitarize;
% decomp = bigrep.decomposition;
% 
% % two random irreps
% rand_comp = decomp.component(randi(decomp.nComponents));
% rand_irr1 = rand_comp.irrep(randi(rand_comp.nIrreps));
% rand_comp = decomp.component(randi(decomp.nComponents));
% rand_irr2 = rand_comp.irrep(randi(rand_comp.nIrreps));
% 
% % actual rep to be decomposed
% rep = kron(rand_irr1, rand_irr2);
% rep = rep.unitarize
% decomp = rep.decomposition
% 
% % basis
% randcomp = decomp.component(randi(decomp.nComponents));
% randirrep = randcomp.irrep(randi(randcomp.nIrreps));
% basis = randirrep.basis;
% 
% % compute size of random set to be symmetrized 
% %          (using p_thr. = 10^-7, notice that basis
% %           is a gobal_dim x irrep_dim matrix)
% numb_group_samples = ceil(7*8*log(10)+2*log(size(basis)(2)))
% subspace_dimension = size(basis)(2)
% 
% % sample random group elements
% i = 1; gens = {};
% while i < numb_group_samples
%   g = Sn.sample;
%   gens{i}=g;
%   if g!=Sn.inverse(g)
%     gens{i+1}=Sn.inverse(g);
%     numb_group_samples+=1;
%     i+=1;
%   endif
%   i+=1;
% endwhile
% 
% % generate group images
% l = size(gens)(2); % gens is a 1 x |gens| matrix
% i = 1;
% gen_ims = {};
% while i < l+1
%   gen_ims{i} = rep.image(gens{i});
%   i+=1;
% endwhile
% 
% % save files: (v7 is used so scipy can read them being octave outputs)
% cd InFiles
% save -v7 basis.mat basis
% save -v7 gen_ims.mat gen_ims
% cd ..

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%
%% Example 3: symmetry group of the I444-222 scenario (3 parties, 4 measurements, 2 outcomes)

disp("Symmetry of the Bell scenario with 3 parties, 4 measurement settings and 2 outcomes.")
disp(" ")
disp("Group = S3 wr S4 wr S2, rep: primitive of the (S4 wr S2)-imprimitive rep.")
disp(" ")

% build group
Parties = replab.S(3); Settings= replab.S(4); Outcomes= replab.S(2);
X = Settings.wreathProduct(Outcomes);
W = Parties.wreathProduct(X)
Xrep= X.imprimitiveRep(Outcomes.naturalRep);
rep = W.primitiveRep(Xrep);
rep = rep.complexification;
rep = rep.unitarize

% decompose
decomp = rep.decomposition

% select some random irrep
randcomp  = decomp.component(randi(decomp.nComponents));
randirrep = randcomp.irrep(randi(randcomp.nIrreps));
basis = randirrep.basis;

% compute size of random set to be symmetrized 
%          (using p_thr. = 10^-7, notice that basis
%           is a gobal_dim x irrep_dim matrix)
numb_group_samples = ceil(7*8*log(10)+2*log(size(basis)(2)))
subspace_dimension = size(basis)(2)

% sample random group elements
i = 1; gens = {};
while i < numb_group_samples
  g = W.sample;
  gens{i}=g;
  % check if g^2 != 1
  if W.isIdentity(W.composeAll({g,g})) == 0
    gens{i+1}=W.inverse(g);
    numb_group_samples+=1;
    i+=1;
  endif
  i+=1;
endwhile

% generate group images
l = size(gens)(2); % gens is a 1 x |gens| matrix
i = 1;
gen_ims = {};
while i < l+1
  gen_ims{i} = rep.image(gens{i});
  i+=1;
endwhile

% save files: (v7 is used so scipy can read them being octave outputs)
cd InFiles
save -v7 basis.mat basis
save -v7 gen_ims.mat gen_ims
cd ..


%%%%%%%%%%%%%%%%%%%%%%
% LIE GROUP EXAMPLES %
%%%%%%%%%%%%%%%%%%%%%%%

% TBD
