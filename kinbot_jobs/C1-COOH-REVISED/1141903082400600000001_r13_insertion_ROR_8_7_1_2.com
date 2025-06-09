%mem=28GB
%chk=1141903082400600000001_r13_insertion_ROR_8_7_1_2
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                 1.6984480000        1.0060460000       -0.1548760000
O                -0.0419020000        1.7420780000        0.5004410000
C                 3.0826610000        1.3155530000       -0.5810260000
F                 4.0054870000        0.7168790000        0.1832830000
F                 3.3390540000        0.9182100000       -1.8351850000
F                 3.3716120000        2.6052380000       -0.5480430000
O                 0.9418320000       -0.2250700000       -0.0349380000
H                -0.0900320000        0.4486580000        0.3790010000

1 2 F
1 3 F
1 7 F
3 4 F
3 5 F
3 6 F
7 8 F


