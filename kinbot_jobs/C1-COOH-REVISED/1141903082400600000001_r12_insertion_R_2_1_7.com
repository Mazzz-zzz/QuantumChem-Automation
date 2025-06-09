%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_2_1_7
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.3514210000       -0.1799210000       -0.1570870000
O                 2.7177890000       -0.6785420000       -0.9776450000
C                -0.1780600000       -0.0162770000       -0.0241380000
F                -0.4992890000        0.9704080000        0.8087290000
F                -0.7318710000        0.2674620000       -1.2002320000
F                -0.7626610000       -1.1061070000        0.4354700000
O                 2.8223090000        0.7809340000        0.2343810000
H                 2.5999840000        1.4663140000        0.8794360000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


