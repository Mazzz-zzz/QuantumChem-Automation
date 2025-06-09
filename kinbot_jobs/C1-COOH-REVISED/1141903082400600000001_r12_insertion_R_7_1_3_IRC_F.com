%mem=28GB
%chk=1141903082400600000001_r12_insertion_R_7_1_3_IRC_F
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
C                 1.7219690000       -0.7156890000       -0.3194690000
O                 2.6963300000       -1.2874570000       -0.1624820000
C                 0.1472720000        0.2378760000       -0.0370400000
F                -0.2719210000        1.1475290000        0.8569330000
F                -0.2840710000        0.5327160000       -1.2304610000
F                -0.5073570000       -0.8624200000        0.4057880000
O                 1.7320080000        1.0154880000       -0.1569900000
H                 2.0854010000        1.4362330000        0.6426320000


