%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_7_1_3
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.6500410000       -0.6124050000        0.0286560000
O                 2.7402100000       -1.0754000000        0.0558130000
C                -0.0056720000        0.0923150000       -0.0158080000
F                -0.2006490000        0.7626200000        1.0554750000
F                -0.2237810000        0.7318460000       -1.1000680000
F                -0.7647850000       -0.9230710000       -0.0071100000
O                 1.6317430000        1.0541170000       -0.0775360000
H                 2.4925240000        1.4742540000        0.0594890000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


