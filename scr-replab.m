% initiate RepLAB in its folder (folder address must be edited in)
cd ../replab-0.9.0;
replab_init
cd ../RepCert

%%%%%%%%%%%%%%%%%%%%%%%%%
% FINITE GROUP EXAMPLES %
%%%%%%%%%%%%%%%%%%%%%%%%%

%
% Example 1: permutation group, tensor power representation

Sn  = replab.S(6)
nat = Sn.naturalRep;
rep = kron(nat,kron(nat,nat)) %4th tensor power of natural rep.
rep = rep.complexification;
rep = rep.unitarize;

% decompose
decomp = rep.decomposition

% select some random irrep
randcomp  = decomp.component(randi(decomp.nComponents));
randirrep = randcomp.irrep(randi(randcomp.nIrreps));
basis = randirrep.basis;

%
% using p_thr. = 10^-7, notice that basis is a gobla_dim x irrep_dim matrix
numb_group_samples = ceil(7*8*log(10)+2*log(size(basis)(2)))

% sample random generators
i = 1; gens = {};
while i < numb_group_samples
  g = Sn.sample;
  gens{i}=g;
  if g!=Sn.inverse(g)
    gens{i+1}=Sn.inverse(g);
    numb_group_samples+=1;
    i+=1;
  endif
  i+=1;
endwhile

l = size(gens)(2); % gens is a 1 x |gens| matrix
i = 1;
gen_ims = {};
while i < l+1
  gen_ims{i} = rep.image(gens{i});
  i+=1;
endwhile



% % save files: (v7 is used so scipy can read them being octave outputs)
save -v7 basis.mat basis
save -v7 gen_ims.mat gen_ims


%
% TBD: multi-partite non-locality symmetry and lie group. 


%
% FINITE GROUP:
%
% 
% % create a group:
% % U  = replab.U(3);
% % Sn = replab.S(3);
% Parties = replab.S(3);
% Settings= replab.S(4);
% Outcomes= replab.S(2);
% X = Settings.wreathProduct(Outcomes);
% W = Parties.wreathProduct(X);
% % W = Sn.wreathProduct(U)
% % W = Sn
% %
% % Set generators:
% % gen1 = [2 1 3 4 5 6 7];
% % gen2 = [2 3 4 5 6 7 1];
% % gens = W.generators;
% 
% % Cayley diam calculation for (Sa wr Sb wr Sc, X := Sb wr Sc):
% % 
% % diam(X) = diam(Sb) + b*diam(Sc) = 7 + 4*1 = 11
% % diam(W) = diam(Sa) + a*diam(X) = 2 + 3*11 = 35
% 
% % create rep:
% Xrep= X.imprimitiveRep(Outcomes.naturalRep);
% rep = W.primitiveRep(Xrep);
% % complexify (if it is real):
% rep = rep.complexification
% 
% % Simultaneously sample generators and set their images:
% %
% % if U has u generators and Sn has 2 generators, then the total number of generators
% % is n*u + 2. (For Sn \wr U.)
% 
% i = 1; 
% % generators = {}; 
% gen_ims={};
% while i < W.nGenerators+1
%   % generators{i} = W.sample;
%   % generators{i+1} = W.inverse(generators{i});
%   gen_ims{i} = rep.image(W.generators{i});
%   i = i+1;
% endwhile
% 
% % Generator images
% % i = 1; %indexing of generators starts with 1
% % gen_ims = {};
% % while i < W.nGenerators+1
% %   gen_ims{i} = rep.image(W.generators{i});
% %   i = i+1;
% % endwhile
% % decompose rep:
% dec = rep.decomposition.nice
% % sample random subrep: (first random isotypic component, then random irrep)
% randcomp  = dec.component(randi(dec.nComponents));
% randirrep = randcomp.irrep(randi(randcomp.nIrreps));
% % basis for irrep:
% basis = randirrep.basis;
% 
% % save files: (v7 is used so scipy can read them being octave outputs)
% save -v7 basis.mat basis
% save -v7 gen_ims.mat gen_ims


%
% LIE GROUP:
% %
% 
% % create a group:
% U  = replab.U(3);
% Sn = replab.S(3);
% W = Sn.wreathProduct(U)
% 
% % create a rep and decompose it:
% Urep = kron(U.definingRep, U.definingRep);
% Wrep = W.imprimitiveRep(Urep)
% Wdec = Wrep.decomposition.nice
% 
% %
% % Sample generators: (UxUxU: Clifford-Phase-gate, Fourier, F_3-generator, Pauli X, and the magic gate, one per copy)
% % So 5*s+2 generators for S(s) wr U(3) 
% %
% nGenBare = 5*3 + 2; % Randomly select gates to get generator set whp.
% nGen = 2*nGenBare;  % Because of symmetrization
% gen_ims = {}; i = 1;
% while i < nGen:
%   gen_ims{i} = Wrep.image(W.sample);
%   gen_ims{i+1} = Wrep.image(W.sample);
%   i = i+2;
% endwhile
% 
% 
% %
% % Sample random irrep:
% %
% randcomp  = Wdec.component(randi(Wdec.nComponents));
% randirrep = randcomp.irrep(randi(randcomp.nIrreps));
% 
% % basis for irrep:
% basis = randirrep.basis;
% 
% % save files: (v7 is used so scipy can read them being octave outputs)
% save -v7 basis.mat basis
% save -v7 gen_ims.mat gen_ims
% % save -v7 cyclic_perm.mat cyclic_perm
% % save -v7 transposition.mat transposition
