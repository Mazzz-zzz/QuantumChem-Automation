%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
freq
opt(CalcFC, Tight)

Gaussian input prepared by ASE

0 2
C                -0.6376500000       -1.3641580000        0.1983100000
F                -0.2914120000       -2.0709300000       -0.8508930000
F                -0.2450100000       -1.9389840000        1.3098940000
F                -1.9287560000       -1.1339560000        0.2120320000


