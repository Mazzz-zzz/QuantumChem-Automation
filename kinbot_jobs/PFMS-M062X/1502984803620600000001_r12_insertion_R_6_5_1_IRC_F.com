%mem=28GB
%chk=1502984803620600000001_r12_insertion_R_6_5_1_IRC_F
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
C                -0.0052520000        0.0040120000       -0.0012150000
F                -0.4755510000        0.5745360000       -1.1030750000
F                -0.4149700000        0.7110040000        1.0443560000
F                -0.4523370000       -1.2274050000        0.0898050000
S                 1.8385720000       -0.0228690000       -0.0515030000
O                 2.2825140000       -0.4926260000        1.2067620000
O                 2.2128380000       -0.6438880000       -1.2661180000
O                 2.1341640000        1.5227100000       -0.1542670000
H                 1.3505370000        2.0873620000       -0.1678650000


