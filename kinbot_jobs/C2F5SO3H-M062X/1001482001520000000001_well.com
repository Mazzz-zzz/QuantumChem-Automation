%mem=28GB
%chk=1001482001520000000001_well
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 1
C                 0.9201470000       -1.8647700000       -0.5901070000
C                 1.6537980000       -0.7771130000       -0.6903810000
F                 1.6586730000        0.1710880000        0.2328790000
F                 2.4503220000       -0.5106660000       -1.6936820000
F                 0.9137970000       -2.8059200000       -1.4991290000
F                 0.1296520000       -2.1085430000        0.4206100000


