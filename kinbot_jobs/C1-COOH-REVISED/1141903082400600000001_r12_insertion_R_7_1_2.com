%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_7_1_2
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.4272390000       -0.0552720000        0.6549870000
O                 2.3546030000       -0.6262830000       -0.7781710000
C                -0.0318710000       -0.0581910000        0.1502470000
F                -0.8245160000        0.6746460000        0.9281000000
F                -0.2205750000        0.4148540000       -1.0789940000
F                -0.5595500000       -1.2674240000        0.1439530000
O                 2.1490930000        1.1758230000       -0.2123250000
H                 3.0251980000        1.2461260000        0.1911160000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


