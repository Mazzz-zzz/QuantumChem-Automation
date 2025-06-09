%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_4_3_5_IRC_R
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
C                 1.8156150000       -0.1585840000        0.2308080000
O                 2.5496660000       -1.0381720000        0.5519240000
C                 0.3442610000       -0.4328310000        0.0408110000
F                -0.4731550000        0.4214000000       -0.2875650000
F                -1.9090270000        1.9180850000       -0.8665080000
F                -0.0794770000       -1.6071190000        0.2268040000
O                 2.0638740000        1.1102010000       -0.0089670000
H                 3.0078690000        1.2913000000        0.1116060000


