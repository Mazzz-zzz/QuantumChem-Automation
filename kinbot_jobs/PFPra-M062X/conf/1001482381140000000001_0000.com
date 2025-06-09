%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                -0.0614980000       -0.7569750000        0.8769280000
C                -1.0826300000        0.4150560000        0.9987790000
F                -2.1441630000        0.3189120000        0.2060860000
F                -1.4943260000        0.4026350000        2.2681150000
F                -0.4730890000        1.5633980000        0.7501760000
F                -0.7395500000       -1.7395480000        0.4033170000


