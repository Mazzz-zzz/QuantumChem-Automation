%mem=28GB
%chk=1141903082400600000001_r13_insertion_ROR_4_3_1_7
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 2.3354770000        1.1635310000       -0.0758970000
O                 3.2816050000        1.8369250000       -0.3006520000
C                 1.6843690000       -0.1311940000       -0.0286140000
F                -0.1849960000        0.5784400000        0.0149040000
F                 1.5839880000       -0.8393490000       -1.0573190000
F                 1.6537760000       -0.7952010000        1.0166340000
O                 0.7668380000        2.2773250000        0.4707610000
H                 1.2004530000        3.1360830000        0.5829860000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


