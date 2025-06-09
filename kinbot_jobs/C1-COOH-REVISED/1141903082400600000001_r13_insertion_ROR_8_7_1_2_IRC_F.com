%mem=28GB
%chk=1141903082400600000001_r13_insertion_ROR_8_7_1_2_IRC_F
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
C                 1.9287290000        1.0591000000       -0.1648150000
O                -0.2247090000        1.0551590000        0.8140150000
C                 3.3898270000        1.1550150000       -0.6239130000
F                 4.2002800000        0.9376410000        0.3875320000
F                 3.6444790000        0.2708800000       -1.5737800000
F                 3.5706570000        2.3751730000       -1.0928870000
O                 0.9805150000        0.7443990000       -0.7107290000
H                -1.1826190000        0.9302260000        0.8732350000


