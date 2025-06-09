%mem=28GB
%chk=1502984803620600000001_r12_insertion_R_9_8_5_IRC_R
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
C                -0.1111040000       -0.0643080000        0.1015360000
F                -0.6680500000        0.6554880000       -0.8521620000
F                -0.6342680000        0.2591290000        1.2678180000
F                -0.3058070000       -1.3465790000       -0.1358470000
S                 1.7004590000        0.2683430000        0.1452340000
O                 2.2429180000       -0.5246360000        1.1784680000
O                 2.1774020000        0.1215180000       -1.2672270000
O                 1.8416590000        1.7595300000        0.1659010000
H                 2.2273070000        1.3843510000       -1.0068430000


