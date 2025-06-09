%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_1_3_4
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.6249560000       -0.1725120000        0.0741940000
O                 2.0788910000       -1.2016420000        0.3970080000
C                 0.0596940000       -0.1754520000       -0.5079140000
F                 0.6142760000        0.6638320000        1.4486230000
F                -0.4643550000        0.8254110000       -1.0194850000
F                -0.7475660000       -1.0485630000       -0.2301980000
O                 2.2412390000        0.9207940000       -0.3278420000
H                 1.9124930000        1.6924080000        0.1645280000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


