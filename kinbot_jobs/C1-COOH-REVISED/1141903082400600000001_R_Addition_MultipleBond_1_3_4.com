%mem=28GB
%chk=1141903082400600000001_R_Addition_MultipleBond_1_3_4
%nprocshared=8
#P mp2/6-31G ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
guess(Mix,Always)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.5871509228       -0.0185857855        0.0151098665
O                 2.2253113883       -0.9500594896        0.3928914202
C                 0.0592121697       -0.0380427454       -0.1141034452
F                -0.0587595260        0.4290616413        1.2144966459
F                -0.5530656394        0.8405654639       -0.8924475978
F                -0.5172249961       -1.2135614140       -0.1685624495
O                 2.0427457682        1.1991855427       -0.2722985759
H                 2.9903524509        1.2972403555       -0.1053620034

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F
1 3 4 F


