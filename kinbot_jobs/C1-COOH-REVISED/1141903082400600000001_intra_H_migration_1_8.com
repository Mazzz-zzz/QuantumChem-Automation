%mem=28GB
%chk=1141903082400600000001_intra_H_migration_1_8
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.4811150000        0.2839990000       -0.0135890000
O                 2.3725980000       -0.5661860000       -0.1203930000
C                -0.0260720000        0.0245200000       -0.0375800000
F                -0.5415300000        0.6746520000        1.1017920000
F                -0.5475670000        0.4308110000       -1.0960920000
F                -0.2944470000       -1.3270410000        0.0273550000
O                 1.9397900000        1.4490910000        0.1278550000
H                 2.9357360000        0.5344280000        0.0095650000



