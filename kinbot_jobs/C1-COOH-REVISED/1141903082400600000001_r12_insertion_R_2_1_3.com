%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_2_1_3
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.4036540000        0.7603670000        0.3677970000
O                 1.6488070000       -0.5657760000       -0.6171630000
C                -0.1116590000       -0.1075490000       -0.0687210000
F                -0.8818350000        0.6891260000        0.5743550000
F                -0.4328250000       -0.0325970000       -1.3051980000
F                -0.2157060000       -1.2586240000        0.4537080000
O                 2.6204070000        1.2670840000        0.5331410000
H                 3.2887810000        0.7522420000        0.0609970000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


