%mem=28GB
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.7671365444        0.0000000000        0.0000000000
O                 2.2494956133       -0.8902015098       -0.6071864280
C                 0.0000000000        0.0000000000        0.0000000000
F                 1.3527865451       -0.2687333099        1.4771027794
F                -0.7593316576        0.9019935091        0.4822364093
F                -0.6267662689       -1.0926288291       -0.0920758650
O                 2.1740288851        1.2809537868        0.0000000000
H                 1.7485476308        1.7588481144       -0.7196030450


