%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_4_3_1_IRC_F
%nprocshared=8
#P M062X/Def2TZVPP ! ASE formatted method and basis
Symm(None)
scf(xqc)
pop(None)
geom(AllCheck,NoKeepConstants)
guess(Read)
irc(RCFC,forward,MaxPoints=100,StepSize=2)

Gaussian input prepared by ASE

0 1
C                 1.6453570000       -0.1341830000        0.2062300000
O                 2.0709480000       -1.2124650000        0.4297020000
C                 0.0128810000       -0.1283010000       -0.4705770000
F                 0.7486710000        0.5321360000        1.2915320000
F                -0.6279990000        0.8858060000       -0.8991110000
F                -0.7900160000       -1.0582920000       -0.1779610000
O                 2.3169680000        0.8928300000       -0.3419720000
H                 1.9428110000        1.7267480000       -0.0389280000


