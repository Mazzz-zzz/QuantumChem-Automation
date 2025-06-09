%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_3_1_2
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.3022810000        0.8322440000        0.3777250000
O                 1.7158980000       -0.6118450000       -0.6140070000
C                -0.0224280000       -0.0889210000       -0.0529630000
F                -0.9528670000        0.6247920000        0.5195900000
F                -0.3351190000       -0.0785140000       -1.3192980000
F                -0.1081220000       -1.2542400000        0.5014120000
O                 2.5324140000        1.3164740000        0.5179810000
H                 3.1875700000        0.7642840000        0.0684750000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


