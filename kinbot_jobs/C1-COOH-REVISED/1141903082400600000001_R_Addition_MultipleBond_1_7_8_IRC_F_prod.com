%mem=28GB
%chk=1141903082400600000001_R_Addition_MultipleBond_1_7_8_IRC_F_prod
%nprocshared=8
#P mp2/6-31G ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
guess(Mix,Always)
freq
opt(CalcFC)

Gaussian input prepared by ASE

0 1
C                 0.9678040000        0.1951320000        0.0445430000
O                 1.7971140000       -0.8065060000       -0.3918740000
C                -0.5509720000       -0.0863120000        0.0063760000
F                -1.1794280000        0.6711760000        0.9982980000
F                -1.0835200000        0.3052380000       -1.2311640000
F                -0.8774880000       -1.4245300000        0.2137350000
O                 1.4488640000        1.2861150000        0.3979700000
H                 2.7208480000       -0.4600690000       -0.3424130000


