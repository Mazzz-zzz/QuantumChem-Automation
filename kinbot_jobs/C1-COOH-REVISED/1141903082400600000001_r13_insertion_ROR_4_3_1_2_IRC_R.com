%mem=28GB
%chk=1141903082400600000001_r13_insertion_ROR_4_3_1_2_IRC_R
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
C                 2.0101600000        1.1679630000        0.4812170000
O                 1.0430210000        0.5907410000       -1.6333240000
C                 1.3044510000       -0.1265620000       -0.7102330000
F                 1.1796690000        2.0480120000        0.9588450000
F                 0.3577390000       -0.6749850000        0.0630450000
F                 2.3256190000       -0.9943160000       -0.7401590000
O                 3.1840580000        1.6453120000        0.3577160000
H                 3.2427640000        2.5883120000        0.6029010000


