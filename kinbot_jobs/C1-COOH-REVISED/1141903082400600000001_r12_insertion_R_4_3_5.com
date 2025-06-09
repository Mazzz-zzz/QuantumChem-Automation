%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_4_3_5
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.5979970000       -0.1197630000        0.0088740000
O                 2.3788580000       -0.8606670000       -0.5539110000
C                 0.2490690000       -0.3474080000        0.2713830000
F                -0.6661390000        1.0165860000        0.5727040000
F                -0.8003870000        0.7701940000       -1.3064640000
F                -0.4262670000       -1.2756300000        0.4562220000
O                 2.0407420000        1.0914710000        0.4321440000
H                 2.9457520000        1.2294960000        0.1179610000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


