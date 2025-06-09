%mem=28GB
%chk=1141903082400600000001_r13_insertion_ROR_4_3_1_2
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 2.0737610000        0.9912590000        0.4049590000
O                 1.1239230000        0.9062560000       -1.3530450000
C                 1.4485140000       -0.0172870000       -0.4283480000
F                 0.9777420000        1.7037220000        0.4752560000
F                 0.4499550000       -0.5812390000        0.1031610000
F                 2.1829090000       -0.9330260000       -0.8662070000
O                 3.2425500000        1.6047060000        0.5049170000
H                 3.1481260000        2.5700860000        0.5393160000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


