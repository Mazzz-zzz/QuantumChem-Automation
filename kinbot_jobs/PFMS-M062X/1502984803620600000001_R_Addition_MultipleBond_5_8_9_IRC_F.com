%mem=28GB
%chk=1502984803620600000001_R_Addition_MultipleBond_5_8_9_IRC_F
%nprocshared=8
#P mp2/6-31G ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
guess(Read,Mix)
geom(AllCheck,NoKeepConstants)
irc(RCFC,forward,MaxPoints=100,StepSize=2)

Gaussian input prepared by ASE

0 1
C                -0.2571190000       -0.1234320000        0.1188930000
F                -0.7448100000        0.6067690000       -0.9340370000
F                -0.7966820000        0.2942380000        1.3135810000
F                -0.4546280000       -1.4718760000       -0.0696410000
S                 1.7051360000        0.1863090000        0.2086660000
O                 2.3257540000       -0.6373580000        1.4132450000
O                 2.3072870000        0.0628310000       -1.3996160000
O                 1.9552480000        1.8797640000        0.0241100000
H                 2.4003780000        1.3871580000       -1.1519240000


