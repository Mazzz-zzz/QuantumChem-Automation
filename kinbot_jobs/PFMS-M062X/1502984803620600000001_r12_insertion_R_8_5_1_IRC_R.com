%mem=28GB
%chk=1502984803620600000001_r12_insertion_R_8_5_1_IRC_R
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
C                -0.1255770000       -0.1075170000        0.0364810000
F                -0.7092400000        0.3675720000       -1.0465740000
F                -0.5986170000        0.5091370000        1.1020460000
F                -0.3589460000       -1.4035060000        0.1337860000
S                 1.6995330000        0.1144640000       -0.0720170000
O                 2.2653520000       -0.2764600000        1.1677830000
O                 2.1393530000       -0.4448000000       -1.2983580000
O                 1.6360110000        1.6858560000       -0.1760330000
H                 2.5226420000        2.0680870000       -0.2502380000


