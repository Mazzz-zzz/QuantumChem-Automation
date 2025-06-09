%mem=28GB
%chk=1141903082400600000001_r13_insertion_CO2_3_8
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.9242520000        0.1731140000       -0.3836390000
O                 1.8930270000       -0.3677690000       -1.3798750000
C                 0.0231520000        0.2717950000        0.2296130000
F                -0.9046300000        0.5717970000        1.0033140000
F                -0.2636820000        0.8085850000       -0.8530180000
F                -0.0380970000       -0.9628200000        0.1063860000
O                 2.3399210000        0.7966410000        0.6786370000
H                 1.0213470000        0.8015360000        0.9681800000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


