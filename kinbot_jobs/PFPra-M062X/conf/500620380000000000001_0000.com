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
C                -0.7886660000       -0.6791460000       -1.7444490000
F                -1.8111980000       -0.4283110000       -2.4961460000
F                -0.6847060000       -1.9684350000       -1.7585820000


