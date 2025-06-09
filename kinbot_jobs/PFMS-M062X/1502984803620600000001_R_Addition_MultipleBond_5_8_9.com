%mem=28GB
%chk=1502984803620600000001_R_Addition_MultipleBond_5_8_9
%nprocshared=8
#P mp2/6-31G ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
guess(Mix,Always)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                -0.1389252385       -0.1011609458        0.0945247263
F                -0.6552143011        0.4999522217       -0.9690054224
F                -0.5969910297        0.4441133886        1.2044391334
F                -0.4121332706       -1.3910838245        0.0680467994
S                 1.6899717174        0.0958878719        0.0485417454
O                 2.2110420764       -0.5515579867        1.1891976505
O                 2.1451379429       -0.2040297094       -1.2615136998
O                 1.7543651427        1.6620804145        0.1744399788
H                 2.4433099884        1.7302031501       -1.0253928925

1 2 F
1 3 F
1 4 F
1 5 F
5 6 F
5 7 F
5 8 F
8 9 F
5 8 9 F


