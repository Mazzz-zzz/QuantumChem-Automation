%mem=28GB
%chk=1141903082400600000001_ketoenol_2_1_3_4
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 0.9648300000        0.2008550000        0.3791000000
O                 0.7106410000       -0.7956000000       -0.2246780000
C                 1.3413170000        1.3563820000       -0.5401610000
F                 1.1941720000        0.0122590000       -1.8749840000
F                 2.5684310000        1.7806020000       -0.6528000000
F                 0.4916070000        2.2543740000       -0.9158360000
O                 1.0336100000        0.3435710000        1.7057320000
H                 0.7938890000       -0.4876670000        2.1373370000



