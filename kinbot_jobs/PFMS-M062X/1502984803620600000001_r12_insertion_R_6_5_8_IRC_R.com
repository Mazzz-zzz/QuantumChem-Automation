%mem=28GB
%chk=1502984803620600000001_r12_insertion_R_6_5_8_IRC_R
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
C                -0.9583010000       -0.1266960000        0.0475150000
F                -1.5137670000        1.0397850000       -0.2400280000
F                -1.3373780000       -0.5060200000        1.2493370000
F                -1.3512960000       -1.0195180000       -0.8405770000
S                 0.9114380000        0.0048850000        0.0010010000
O                 1.3603330000       -0.0999750000        1.3353420000
O                 1.3556190000       -0.8395850000       -1.0497700000
O                 1.0986320000        1.5031950000       -0.4355080000
H                 1.1754890000        1.5656840000       -1.3981110000


