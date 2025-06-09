%mem=28GB
%chk=1502984803620600000001_R_Addition_MultipleBond_5_1_2
%nprocshared=8
#P mp2/6-31G ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
guess(Mix,Always)
opt(NoFreeze,TS,CalcAll,NoEigentest,MaxCycle=999)

Gaussian input prepared by ASE

0 1
C                -0.0243716708       -0.1207720959        0.1452799291
F                -0.1582885555        0.6205422822       -1.0500477592
F                -0.6310865358        0.5358163180        1.1083245192
F                -0.5131725742       -1.3161726853       -0.0666249659
S                 1.7986785515        0.0334262797        0.0363899407
O                 2.4053254269       -0.4552555991        1.2158552706
O                 2.1744245720       -0.4339629425       -1.2503212424
O                 1.8710763181        1.6048396051        0.1023387861
H                 1.9768633533        2.1161642848       -0.7122190641

1 2 F
1 3 F
1 4 F
1 5 F
5 6 F
5 7 F
5 8 F
8 9 F
5 1 2 F


