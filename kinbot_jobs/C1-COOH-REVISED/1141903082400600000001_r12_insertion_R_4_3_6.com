%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_4_3_6
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999,Cartesian)

Gaussian input prepared by ASE

0 1
C                 1.6638090000        0.2912470000        0.1854990000
O                 2.1300210000       -0.6961190000        0.6511630000
C                 0.1779120000        0.4674130000        0.0982910000
F                -0.5648120000       -0.3412760000        0.6413120000
F                -0.3486670000        1.1786350000       -0.8205780000
F                -1.2595350000       -1.9625380000       -0.1868660000
O                 2.2821810000        1.3540970000       -0.3094640000
H                 3.2387090000        1.2128180000       -0.2604490000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


