%mem=28GB
%chk=1502984803620600000001_r13_insertion_ROR_2_1_5_6_IRC_F
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
C                 2.0379280000       -0.2921500000       -0.3170320000
F                -0.3250710000        0.9954020000        0.4746740000
F                 1.9911240000       -0.9999310000        0.7820190000
F                 1.1965550000       -0.7508080000       -1.2086780000
S                 2.0774770000        1.4441150000       -0.0723020000
O                 0.8648610000        2.1885060000        0.4010750000
O                 3.2408290000        1.7452290000        0.6773610000
O                 2.1626690000        1.9246480000       -1.5522900000
H                 3.0368120000        1.7161140000       -1.9156150000


