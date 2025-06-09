%mem=28GB
%chk=1141903082400600000001_intra_H_migration_2_8
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.3343220000       -0.2196740000       -0.5421630000
O                 1.5534820000       -0.4835480000       -1.6795490000
C                 1.8776190000       -0.7629040000        0.7970550000
F                 2.6427700000       -1.8396460000        0.6371640000
F                 2.6277190000        0.1363010000        1.4288770000
F                 0.9136040000       -1.1086270000        1.6288470000
O                 0.4312250000        0.7453880000       -0.6794710000
H                 0.7368970000        0.3895410000       -1.7839780000



