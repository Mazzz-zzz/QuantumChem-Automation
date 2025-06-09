%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_8_7_1
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.4907020000        0.2356100000       -0.0174680000
O                 2.1817410000       -0.6898710000       -0.4103140000
C                -0.0774000000       -0.0077770000        0.0098580000
F                -0.6896820000        0.7071030000        0.9455390000
F                -0.6421250000        0.3342790000       -1.1414750000
F                -0.3903940000       -1.2537890000        0.2321120000
O                 1.8877370000        1.1999680000        0.2996390000
H                 3.5590470000        0.9787500000        0.0810240000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


