%mem=28GB
%chk=1141903082400600000001_R_Addition_MultipleBond_1_7_8_IRC_F
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
C                 1.4568580000        0.2193740000        0.0236820000
O                 2.3243170000       -0.6776620000       -0.3780970000
C                -0.0374310000        0.0117970000        0.0089770000
F                -0.6538950000        0.7689950000        1.0019980000
F                -0.5584860000        0.4020520000       -1.2301080000
F                -0.3548080000       -1.3283610000        0.2156570000
O                 2.0365290000        1.3404130000        0.3784190000
H                 3.0494510000        0.4632410000       -0.0210130000


