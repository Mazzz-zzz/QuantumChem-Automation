%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_4_3_1
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.9772760000       -0.1990220000        0.1814730000
O                 2.2664920000       -1.2581620000        0.4817110000
C                -0.1391140000       -0.0395650000       -0.3977000000
F                 0.4344500000        0.4190480000        1.1021660000
F                -0.5558820000        0.9323490000       -0.7821080000
F                -0.8269650000       -0.8945740000       -0.1516300000
O                 2.4297910000        0.9441910000       -0.1991570000
H                 1.7335730000        1.6000140000       -0.2358390000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


