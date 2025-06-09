%mem=28GB
%chk=1502984803620600000001_r12_insertion_R_2_1_5_IRC_F
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
C                -0.1157770000       -0.5833110000        0.3216030000
F                 0.0443780000        1.1651450000       -0.1934540000
F                -0.7748360000       -0.5070260000        1.4082780000
F                -0.8333140000       -1.0932950000       -0.5992420000
S                 1.6335820000        0.3041310000        0.0199800000
O                 2.0444080000        0.1537170000        1.3701320000
O                 1.9324540000       -0.4917660000       -1.1260450000
O                 2.2965600000        1.7089790000       -0.3255600000
H                 2.2430590000        1.8562630000       -1.2788040000


