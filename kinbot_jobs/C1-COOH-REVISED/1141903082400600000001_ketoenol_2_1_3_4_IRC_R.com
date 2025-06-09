%mem=28GB
%chk=1141903082400600000001_ketoenol_2_1_3_4_IRC_R
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
C                 0.8754990000        0.5133870000        0.2122940000
O                -0.0318110000       -0.0777660000       -0.3522280000
C                 1.2324410000        1.7889890000       -0.2947860000
F                 1.1678200000       -1.5520970000       -0.7785500000
F                 1.9708230000        2.6064060000        0.3445790000
F                 0.7059380000        2.2889080000       -1.3359610000
O                 1.5878550000        0.0289200000        1.2152790000
H                 1.5899330000       -0.9319710000        1.0030830000


