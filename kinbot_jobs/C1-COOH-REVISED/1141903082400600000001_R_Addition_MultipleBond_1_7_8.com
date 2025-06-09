%mem=28GB
%chk=1141903082400600000001_R_Addition_MultipleBond_1_7_8
%nprocshared=8
#P mp2/6-31G ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
guess(Mix,Always)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.4901159394        0.0434683971        0.0003957657
O                 2.1843672955       -0.9205421764        0.0027268107
C                -0.0529253756       -0.0093827335       -0.0000482714
F                -0.5288849796        0.6056070972        1.0796043277
F                -0.5280629541        0.6004620122       -1.0829846692
F                -0.4617885829       -1.2637953311        0.0027808775
O                 1.9255083877        1.2989397561       -0.0021886132
H                 3.2342064376        0.8450914240       -0.0007702286

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F
1 7 8 F


