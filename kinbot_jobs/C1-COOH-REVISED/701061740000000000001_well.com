%mem=28GB
%chk=701061740000000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                -0.9958980000        0.1697360000        0.5272800000
F                -2.3016720000        0.1333260000        0.7671020000
F                -0.8024720000        0.7513920000       -0.6575890000
F                -0.5487340000       -1.0843330000        0.4447880000
H                -0.4689140000        0.7119950000        1.3085560000


