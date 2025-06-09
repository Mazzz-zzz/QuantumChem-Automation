%mem=28GB
%chk=1502984803620600000001_r13_insertion_ROR_9_8_5_6_IRC_R
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
geom(AllCheck,NoKeepConstants)
guess(Read)
irc(RCFC,reverse,MaxPoints=100,StepSize=2)

Gaussian input prepared by ASE

0 1
C                 3.3658830000        0.4989870000        1.2483850000
F                 3.7387360000       -0.6552250000        0.7550740000
F                 3.0004540000        0.3795870000        2.5065750000
F                 4.3845030000        1.3431300000        1.1695100000
S                 1.8833260000        1.7523950000        0.1568710000
O                -0.0232590000        1.1437910000       -0.3445480000
O                 2.4641560000        1.9718780000       -1.1218720000
O                 1.4357830000        0.3268980000        0.4037060000
H                -0.5866000000        1.1378450000        0.4413540000


