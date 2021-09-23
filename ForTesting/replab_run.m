% initiate RepLAB in its folder (folder address must be edited in)
cd ../../replab-0.9.0;
replab_init
mkdir ../RepCert/ForTesting/S3wrS3wrS3;
cd ../RepCert/ForTesting/S3wrS3wrS3;


disp("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
disp("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
% build group
Parties = replab.S(3) 
Settings= replab.S(3) 
Outcomes= replab.S(3)
% wreath product is the other way around in replab: G wr H is written H.wreathProduct(G)
% e.g. notice that in the "CH CHSH symmetry" paper of Denis, the representation starts
% with "imprimitive rep of the natural rep of S_outcomes."
X = Settings.wreathProduct(Outcomes);
W = Parties.wreathProduct(X)
Xrep= X.imprimitiveRep(Outcomes.naturalRep);
rep = W.primitiveRep(Xrep);
rep = rep.complexification;
rep = rep.unitarize

% decompose
decomp = rep.decomposition

% loop through isotypic components,
i=1;
dmax = 1;
while i < decomp.nComponents+1
  comp=decomp.component(i);
  j = 1;
  while j < comp.nIrreps+1
    irrep = comp.irrep(j);
    basis = irrep.basis;
    d = size(basis)(2);
    if (d > dmax)
      dmax=d;
    endif
    fname = strcat(int2str(d),'_',int2str(i),'_',int2str(j),'.mat');
    save("-v7",fname,"basis")
    j+=1;
  endwhile
  i+=1;
endwhile

% compute size of random set to be symmetrized 
%          (using p_thr. = 10^-7, notice that basis
%           is a gobal_dim x irrep_dim matrix)
numb_group_samples = ceil(7*8*log(10)+2*log(dmax))

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

% save generators
save -v7 gen_ims.mat gen_ims

