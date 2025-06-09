%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_1_3_4_IRC_F
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
C                 1.6384730000       -0.1270260000        0.2389190000
O                 2.0678740000       -1.2024480000        0.4688900000
C                 0.0426810000       -0.1339090000       -0.5201410000
F                 0.6786280000        0.5110950000        1.2864090000
F                -0.5899940000        0.8774150000       -0.9669910000
F                -0.7605690000       -1.0790240000       -0.2820260000
O                 2.3220160000        0.9169780000       -0.2603090000
H                 1.9205180000        1.7411940000        0.0341620000


